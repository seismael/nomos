#!/usr/bin/env python3
"""validate-registry.py — Validate registry.yaml against schema and consistency rules."""

import sys
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

try:
    from jsonschema import validate as schema_validate, ValidationError
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / ".agents" / "registry.yaml"
SCHEMA_PATH = ROOT / ".agents" / "schema" / "registry.schema.json"
AGENTS_DIR = ROOT / ".agents"

VALID_ROLES = {"capability", "convention", "config", "orchestration"}
VALID_MODES = {"workflow", "skill", "persona", None, ""}
VALID_STATUSES = {"active", "deprecated", "retired"}
VALID_COSTS = {"low", "medium", "high"}


def load_registry():
    if not REGISTRY_PATH.exists():
        print(f"ERROR: {REGISTRY_PATH} not found")
        sys.exit(1)
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate(registry):
    errors = []
    warnings = []

    # JSON Schema validation
    if SCHEMA_PATH.exists():
        try:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                schema = json.load(f)
            schema_validate(instance=registry, schema=schema)
        except ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
        except json.JSONDecodeError as e:
            errors.append(f"Schema file is invalid JSON: {e}")
    else:
        warnings.append(
            f"Schema file not found: {SCHEMA_PATH}. Skipping schema validation."
        )

    for field in [
        "version",
        "framework_version",
        "active_profile",
        "layers",
        "artifacts",
    ]:
        if field not in registry:
            errors.append(f"Missing required field: {field}")

    if "active_profile" in registry:
        valid = {"minimal", "standard", "full"}
        if registry["active_profile"] not in valid:
            errors.append(f"Invalid active_profile: {registry['active_profile']}")

    if "layers" in registry:
        layer_ids = set()
        for layer in registry["layers"]:
            lid = layer.get("id")
            if lid in layer_ids:
                errors.append(f"Duplicate layer id: {lid}")
            layer_ids.add(lid)

    if "artifacts" not in registry:
        errors.append("No artifacts defined")
        return errors, warnings

    artifacts = registry["artifacts"]
    paths_seen = set()
    trigger_map = {}

    for i, artifact in enumerate(artifacts):
        idx = f"artifact[{i}]"

        for field in [
            "path",
            "role",
            "triggers",
            "layer",
            "priority",
            "status",
            "context_cost",
        ]:
            if field not in artifact:
                errors.append(f"{idx}: missing required field '{field}'")

        path = artifact.get("path", "")
        if path:
            if path in paths_seen:
                errors.append(f"{idx}: duplicate path '{path}'")
            paths_seen.add(path)
            full_path = AGENTS_DIR / path
            if not full_path.exists():
                errors.append(f"{idx}: path does not exist: {full_path}")

        role = artifact.get("role", "")
        if role and role not in VALID_ROLES:
            errors.append(f"{idx}: invalid role '{role}'")

        mode = artifact.get("mode", "")
        if mode and mode not in VALID_MODES:
            errors.append(f"{idx}: invalid mode '{mode}'")

        status = artifact.get("status", "")
        if status and status not in VALID_STATUSES:
            errors.append(f"{idx}: invalid status '{status}'")
        if status == "retired":
            warnings.append(f"{idx}: artifact is retired: {path}")
        elif status == "deprecated":
            warnings.append(f"{idx}: artifact is deprecated: {path}")
            if "superseded_by" not in artifact:
                warnings.append(f"{idx}: deprecated artifact missing 'superseded_by'")

        cost = artifact.get("context_cost", "")
        if cost and cost not in VALID_COSTS:
            errors.append(f"{idx}: invalid context_cost '{cost}'")

        priority = artifact.get("priority")
        if priority is not None and (
            not isinstance(priority, int) or priority < 1 or priority > 100
        ):
            errors.append(f"{idx}: priority must be 1-100, got {priority}")

        # duplicate trigger check
        triggers = artifact.get("triggers", {})
        if triggers:
            key = (
                artifact.get("layer", ""),
                artifact.get("priority", 0),
                str(triggers.get("phase", "*")),
                str(triggers.get("type", "*")),
                str(triggers.get("complexity", "*")),
            )
            if key in trigger_map:
                errors.append(
                    f"{idx}: duplicate trigger at layer={key[0]} priority={key[1]}: "
                    f"'{trigger_map[key]}' and '{path}'"
                )
            trigger_map[key] = path

    # check depends_on references
    for i, artifact in enumerate(artifacts):
        for dep in artifact.get("depends_on", []):
            if dep not in paths_seen:
                errors.append(
                    f"artifact[{i}]: depends_on '{dep}' not found in registry"
                )

    # check project overrides don't target non-overridable base
    non_overridable = {
        a["path"]
        for a in artifacts
        if a["path"].startswith("base/") and not a.get("overridable", True)
    }
    for i, a in enumerate(artifacts):
        if a.get("path", "").startswith("project/") and "overridable" not in a:
            base_path = a["path"].replace("project/", "base/")
            if base_path in non_overridable:
                errors.append(
                    f"artifact[{i}]: project override targets non-overridable base artifact '{base_path}'"
                )

    return errors, warnings


def main():
    print(f"Validating: {REGISTRY_PATH}")
    registry = load_registry()
    errors, warnings = validate(registry)

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)

    print(f"\nOK — {len(registry.get('artifacts', []))} artifacts validated")
    sys.exit(0)


if __name__ == "__main__":
    main()
