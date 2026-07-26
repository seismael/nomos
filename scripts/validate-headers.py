#!/usr/bin/env python3
"""validate-headers.py — Validate YAML frontmatter in all .agents/ .md files."""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / ".agents"

REQUIRED = {"role", "triggers", "layer", "priority", "status", "context_cost"}
VALID_ROLES = {"capability", "convention", "config", "orchestration"}
VALID_STATUSES = {"active", "deprecated", "retired"}
VALID_COSTS = {"low", "medium", "high"}


def extract_frontmatter(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return None, str(e)

    if not content.startswith("---"):
        return None, "missing frontmatter (must start with ---)"

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "unclosed frontmatter"

    try:
        return yaml.safe_load(parts[1]), None
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"


def main():
    print("Validating frontmatter headers...")
    count = 0
    errors = []

    SKIP_FILES = {"bootstrap.md"}

    for md_file in sorted(AGENTS_DIR.rglob("*.md")):
        if md_file.name in SKIP_FILES:
            continue

        rel = str(md_file.relative_to(ROOT))
        count += 1

        fm, parse_err = extract_frontmatter(md_file)
        if parse_err:
            errors.append(f"{rel}: {parse_err}")
            continue
        if fm is None:
            errors.append(f"{rel}: no frontmatter found")
            continue

        missing = REQUIRED - set(fm.keys())
        if missing:
            errors.append(f"{rel}: missing fields: {missing}")

        if fm.get("role") not in VALID_ROLES:
            errors.append(f"{rel}: invalid role '{fm.get('role')}'")
        if fm.get("status") not in VALID_STATUSES:
            errors.append(f"{rel}: invalid status '{fm.get('status')}'")
        if fm.get("context_cost") not in VALID_COSTS:
            errors.append(f"{rel}: invalid context_cost '{fm.get('context_cost')}'")

        p = fm.get("priority")
        if p is not None and (not isinstance(p, int) or p < 1 or p > 100):
            errors.append(f"{rel}: priority must be 1-100, got {p}")

    print(f"Checked {count} files")
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    print("OK — all frontmatter valid")
    sys.exit(0)


if __name__ == "__main__":
    main()
