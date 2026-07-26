#!/usr/bin/env python3
"""validate-cascade.py — Validate that all trigger combinations resolve to mandatory layers."""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / ".agents" / "registry.yaml"

PHASES = ["plan", "design", "implement", "test", "review", "deploy"]
TYPES = ["feature", "bugfix", "refactor", "architecture", "research", "docs", "ops"]
COMPLEXITIES = ["trivial", "standard", "complex", "critical"]


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def match_trigger_specific(artifact_triggers, phase, task_type, complexity):
    """Like match_trigger but only matches if >=2 dimensions are non-wildcard."""
    t = artifact_triggers or {}
    specific_count = 0

    for dim_key, dim_val in [
        ("phase", phase),
        ("type", task_type),
        ("complexity", complexity),
    ]:
        av = t.get(dim_key)
        if av and av != "*":
            specific_count += 1
            if isinstance(av, list):
                if dim_val not in av:
                    return False
            elif av != dim_val:
                return False
    return specific_count >= 2


def match_trigger(artifact_triggers, phase, task_type, complexity):
    t = artifact_triggers or {}

    art_phase = t.get("phase")
    if art_phase and art_phase != "*":
        if isinstance(art_phase, list):
            if phase not in art_phase:
                return False
        elif art_phase != phase:
            return False

    art_type = t.get("type")
    if art_type and art_type != "*":
        if isinstance(art_type, list):
            if task_type not in art_type:
                return False
        elif art_type != task_type:
            return False

    art_complexity = t.get("complexity")
    if art_complexity and art_complexity != "*":
        if isinstance(art_complexity, list):
            if complexity not in art_complexity:
                return False
        elif art_complexity != complexity:
            return False

    return True


def main():
    print(f"Validating cascade coverage: {REGISTRY_PATH}")
    registry = load_registry()

    layers = registry.get("layers", [])
    mandatory = {l["id"] for l in layers if l.get("mandatory", False)}
    # L4 is not required for trivial complexity — trivial tasks skip gates
    TRIVIAL_SKIP_LAYERS = {"L4"}
    artifacts = registry.get("artifacts", [])

    errors = []
    stats = {"total": 0, "resolved": 0, "valid_gaps": 0, "invalid_gaps": 0}

    for phase in PHASES:
        for task_type in TYPES:
            for complexity in COMPLEXITIES:
                stats["total"] += 1

                LAYER_MAP = {
                    "base": "L1",
                    "phase": "L2",
                    "type": "L3",
                    "complexity": "L4",
                    "project": "L5",
                }

                resolved = set()
                for a in artifacts:
                    if a.get("status") == "retired":
                        continue
                    if match_trigger(
                        a.get("triggers", {}), phase, task_type, complexity
                    ):
                        lid = LAYER_MAP.get(a.get("layer", ""), a.get("layer", ""))
                        resolved.add(lid)

                effective_mandatory = (
                    mandatory - TRIVIAL_SKIP_LAYERS
                    if complexity == "trivial"
                    else mandatory
                )
                missing = effective_mandatory - resolved
                if missing:
                    has_valid = any(
                        a.get("triggers", {}).get("valid") is True
                        and match_trigger_specific(
                            a.get("triggers", {}), phase, task_type, complexity
                        )
                        for a in artifacts
                    )
                    if has_valid:
                        errors.append(
                            f"[{phase},{task_type},{complexity}] marked valid but missing mandatory layers: {missing}"
                        )
                        stats["valid_gaps"] += 1
                    else:
                        stats["invalid_gaps"] += 1
                else:
                    stats["resolved"] += 1

    print(
        f"Combinations: {stats['total']} total | {stats['resolved']} resolved | {stats['valid_gaps']} valid with gaps | {stats['invalid_gaps']} unmarked"
    )
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    print("\nOK — all valid trigger combinations resolve to mandatory layers")
    sys.exit(0)


if __name__ == "__main__":
    main()
