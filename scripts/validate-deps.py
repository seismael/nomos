#!/usr/bin/env python3
"""validate-deps.py — Validate dependency graph has no cycles and all targets exist."""

import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / ".agents" / "registry.yaml"


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_graph(artifacts):
    graph = defaultdict(list)
    all_paths = set()
    for a in artifacts:
        path = a.get("path", "")
        if not path:
            continue
        all_paths.add(path)
        if a.get("status") == "retired":
            continue
        for dep in a.get("depends_on", []):
            graph[path].append(dep)
    return graph, all_paths


def find_cycle(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if color.get(neighbor, WHITE) == GRAY:
                return [node, neighbor]
            if color.get(neighbor, WHITE) == WHITE:
                cycle = dfs(neighbor)
                if cycle:
                    cycle.insert(0, node)
                    return cycle
        color[node] = BLACK
        return None

    for node in graph:
        if color.get(node, WHITE) == WHITE:
            cycle = dfs(node)
            if cycle:
                return " → ".join(cycle)

    return None


def main():
    print("Validating dependency graph...")
    registry = load_registry()
    artifacts = registry.get("artifacts", [])
    graph, all_paths = build_graph(artifacts)

    errors = []
    for source, deps in graph.items():
        for dep in deps:
            if dep not in all_paths:
                errors.append(f"{source}: depends_on '{dep}' not found in registry")

    cycle = find_cycle(graph)
    if cycle:
        errors.append(f"Circular dependency: {cycle}")

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    print("OK — dependency graph is acyclic with valid references")
    sys.exit(0)


if __name__ == "__main__":
    main()
