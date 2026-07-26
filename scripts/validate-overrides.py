#!/usr/bin/env python3
"""validate-overrides.py — Validate project overrides don't violate base artifact contracts."""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / ".agents" / "registry.yaml"
VALID_STRATEGIES = {"replace", "extend", "prepend"}


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate(registry):
    artifacts = registry.get("artifacts", [])
    errors = []
    warnings = []

    base_artifacts = {}
    project_artifacts = {}

    for a in artifacts:
        path = a.get("path", "")
        if not path:
            continue
        if path.startswith("base/"):
            base_artifacts[path] = a
        elif path.startswith("project/"):
            project_artifacts[path] = a

    # Check: no project artifact targets a non-overridable base artifact
    non_overridable = {
        path: a for path, a in base_artifacts.items() if a.get("overridable") is False
    }

    for proj_path, proj_artifact in project_artifacts.items():
        base_path = proj_path.replace("project/", "base/")
        if base_path in non_overridable:
            errors.append(
                f"{proj_path}: overrides non-overridable base artifact '{base_path}'. "
                "Either set overridable: true on the base artifact or remove the project override."
            )

    # Check: project overrides have valid override_strategy
    for proj_path, proj_artifact in project_artifacts.items():
        strategy = proj_artifact.get("override_strategy", "replace")
        if strategy not in VALID_STRATEGIES:
            errors.append(
                f"{proj_path}: invalid override_strategy '{strategy}'. Must be one of {VALID_STRATEGIES}."
            )

    # Check: base artifacts have valid override_strategy
    for base_path, base_artifact in base_artifacts.items():
        strategy = base_artifact.get("override_strategy")
        if strategy and strategy not in VALID_STRATEGIES:
            errors.append(
                f"{base_path}: invalid override_strategy '{strategy}'. Must be one of {VALID_STRATEGIES}."
            )

    # Check: overridable:false base artifacts with project overrides detected above.
    # Warn about project overrides that have no corresponding base artifact.
    for proj_path, proj_artifact in project_artifacts.items():
        base_path = proj_path.replace("project/", "base/")
        strategy = proj_artifact.get("override_strategy")
        if strategy and base_path not in base_artifacts:
            warnings.append(
                f"{proj_path}: has override_strategy='{strategy}' but no matching "
                f"base artifact at '{base_path}'. Override has no effect. "
                "Either remove override_strategy or create the base artifact."
            )

    # Check: deprecated/retired base artifacts with active overrides
    for proj_path, proj_artifact in project_artifacts.items():
        base_path = proj_path.replace("project/", "base/")
        base = base_artifacts.get(base_path)
        if base and base.get("status") in ("deprecated", "retired"):
            warnings.append(
                f"{proj_path}: overrides {base.get('status')} base artifact '{base_path}'. "
                "Consider updating to the superseded version if available."
            )

    return errors, warnings


def main():
    print(f"Validating project overrides: {REGISTRY_PATH}")
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

    print("\nOK — all project overrides are valid")
    sys.exit(0)


if __name__ == "__main__":
    main()
