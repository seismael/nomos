#!/usr/bin/env python3
"""run-compliance-tests.py — Validate behavioral test scenarios against the registry."""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / ".agents" / "registry.yaml"
SCENARIOS_PATH = ROOT / "scripts" / "tests" / "scenarios.yaml"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def match_trigger(artifact_triggers, task_triggers):
    t = artifact_triggers or {}

    for dim in ["phase", "type", "complexity"]:
        av = t.get(dim)
        tv = task_triggers.get(dim)
        if av and av != "*" and tv:
            if isinstance(av, list):
                if tv not in av:
                    return False
            elif av != tv:
                return False
    return True


def get_gates_for_complexity(registry, complexity):
    gates_yaml = next(
        (
            a
            for a in registry.get("artifacts", [])
            if a.get("path") == "base/orchestration/gates.yaml"
        ),
        None,
    )
    if not gates_yaml:
        return []

    gates_path = ROOT / ".agents" / "base" / "orchestration" / "gates.yaml"
    if not gates_path.exists():
        return []

    gates_data = load_yaml(gates_path)
    gate_def = gates_data.get("gates", {}).get(complexity, {})
    return [c["id"] for c in gate_def.get("checkpoints", []) if c.get("required")]


def run():
    print(f"Loading registry: {REGISTRY_PATH}")
    registry = load_yaml(REGISTRY_PATH)
    scenarios = load_yaml(SCENARIOS_PATH)
    artifacts = registry.get("artifacts", [])

    passed = 0
    failed = 0

    for scenario in scenarios["scenarios"]:
        name = scenario["name"]
        triggers = scenario["triggers"]
        expected_paths = set(scenario.get("expected_artifacts", []))
        expected_gates = set(scenario.get("expected_gates", []))

        matched = [
            a
            for a in artifacts
            if a.get("status") != "retired"
            and match_trigger(a.get("triggers", {}), triggers)
        ]
        matched_paths = {a.get("path", "") for a in matched}

        complexity = triggers.get("complexity", "trivial")
        actual_gates = set(get_gates_for_complexity(registry, complexity))

        errors = []

        # Check exact artifact paths
        if expected_paths:
            missing = expected_paths - matched_paths
            if missing:
                errors.append(f"missing artifacts: {sorted(missing)}")
            unexpected = matched_paths - expected_paths
            if unexpected:
                errors.append(f"unexpected artifacts: {sorted(unexpected)}")

        # Check gates
        gate_missing = expected_gates - actual_gates
        if gate_missing:
            errors.append(f"missing gates: {gate_missing}")
        gate_extra = actual_gates - expected_gates
        if gate_extra:
            errors.append(f"unexpected gates: {gate_extra}")

        if errors:
            print(f"FAIL: {name}")
            for e in errors:
                print(f"      {e}")
            failed += 1
        else:
            print(
                f"PASS: {name} ({len(matched)} artifacts, gates={sorted(actual_gates)})"
            )
            passed += 1

    print(f"\n{passed} passed, {failed} failed, {len(scenarios['scenarios'])} total")
    return int(failed > 0)


if __name__ == "__main__":
    sys.exit(run())
