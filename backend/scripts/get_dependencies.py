#!/usr/bin/env python3

import ast
import sys
from collections import defaultdict
from pathlib import Path


class DependencyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.dependencies = {}

    def visit_FunctionDef(self, node):
        self._process_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._process_function(node)
        self.generic_visit(node)

    def _process_function(self, node):
        for decorator in node.decorator_list:

            if not (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr == "dependency"
            ):
                continue

            # Verify pytest.mark.dependency
            mark = decorator.func.value

            if not (
                isinstance(mark, ast.Attribute)
                and mark.attr == "mark"
                and isinstance(mark.value, ast.Name)
                and mark.value.id == "pytest"
            ):
                continue

            name = None
            depends = []

            for kw in decorator.keywords:

                if kw.arg == "name":
                    if isinstance(kw.value, ast.Constant):
                        name = kw.value.value

                elif kw.arg == "depends":

                    if isinstance(kw.value, (ast.List, ast.Tuple)):
                        for item in kw.value.elts:
                            if isinstance(item, ast.Constant):
                                depends.append(item.value)

            if not name:
                continue

            self.dependencies[name] = depends


def parse_file(path):
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        visitor = DependencyVisitor()
        visitor.visit(tree)

        return visitor.dependencies

    except Exception as e:
        print(f"Could not parse {path}: {e}")
        return {}


def build_graph(root_dir):
    """
    dependency_map:
        test -> tests it depends on

    graph:
        dependency -> tests that depend on it
    """

    dependency_map = {}

    for file in Path(root_dir).rglob("*.py"):

        deps = parse_file(file)

        for test_name, depends_on in deps.items():
            dependency_map[test_name] = depends_on

    graph = defaultdict(set)

    for test, deps in dependency_map.items():

        graph.setdefault(test, set())

        for dep in deps:
            graph[dep].add(test)

    return dependency_map, graph


def detect_cycle(graph):
    WHITE = 0
    GRAY = 1
    BLACK = 2

    colors = defaultdict(int)
    stack = []

    def dfs(node):

        colors[node] = GRAY
        stack.append(node)

        for neighbor in graph[node]:

            if colors[neighbor] == GRAY:

                idx = stack.index(neighbor)
                cycle = stack[idx:] + [neighbor]

                return cycle

            if colors[neighbor] == WHITE:

                result = dfs(neighbor)

                if result:
                    return result

        stack.pop()

        colors[node] = BLACK

        return None

    for node in graph:

        if colors[node] == WHITE:

            result = dfs(node)

            if result:
                return result

    return None


def build_removal_order(graph):
    """
    Remove leaf nodes first.

    A leaf node is a node with no dependents.
    """

    graph = {k: set(v) for k, v in graph.items()}

    all_nodes = set(graph)

    for children in graph.values():
        all_nodes.update(children)

    for node in all_nodes:
        graph.setdefault(node, set())

    ordered = []

    while graph:

        leaf_nodes = sorted(
            node for node, dependents in graph.items() if len(dependents) == 0
        )

        if not leaf_nodes:
            raise RuntimeError("Cycle detected")

        ordered.extend(leaf_nodes)

        for leaf in leaf_nodes:
            del graph[leaf]

        for dependents in graph.values():
            dependents.difference_update(leaf_nodes)

    return ordered


def print_dependency_graph(graph):

    print("\nDependency graph:\n")

    for dependency in sorted(graph):

        for dependent in sorted(graph[dependency]):

            print(f"{dependency} -> {dependent}")


def main(root_dir):

    dependency_map, graph = build_graph(root_dir)

    if not dependency_map:
        print("No pytest dependencies found.")
        return

    cycle = detect_cycle(graph)

    if cycle:

        print("\nCircular dependency detected:\n")
        print(" -> ".join(cycle))

        sys.exit(1)

    print_dependency_graph(graph)

    order = build_removal_order(graph)

    print("\nSuggested order to remove dependencies:\n")

    for i, test in enumerate(order, start=1):
        print(f"{i:3}. {test}")

    print("\nSummary:\n")

    print(f"Tests with dependencies: {len(dependency_map)}")

    relationship_count = sum(len(v) for v in dependency_map.values())

    print(f"Dependency relationships: {relationship_count}")


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("Usage:\n" "python test_dependency_order.py <directory>")

        sys.exit(1)

    main(sys.argv[1])

#     1. connectivity-fail-all
#   2. connectivity-failure
#   3. connectivity-success-ood
#   4. external-identifier-failure
#   5. log-first-fail-all
#   6. log-last-fail-all
#   7. log-last-success-2
#   8. merge-software-by-id-fail-different-types
#   9. merge-software-by-id-fail-not-found
#  10. merge-software-by-id-fail-same-id
#  11. property-popularity-fail-all
#  12. property-popularity-failure
#  13. quantity-fail-all
#  14. quantity-failure
#  15. recent-changes-fail-all
#  16. recent-changes-query-success
#  17. remove-wikibase-article-path
#  18. remove-wikibase-language-1
#  19. remove-wikibase-language-3
#  20. remove-wikibase-sparql-frontend-url
#  21. software-version-fail-all
#  22. software-version-failure
#  23. sort-cat-asc
#  24. sort-cat-desc
#  25. sort-edits-asc
#  26. sort-edits-desc
#  27. sort-title-asc
#  28. sort-title-desc
#  29. sort-trip-asc
#  30. sort-trip-desc
#  31. sort-type-asc
#  32. sort-type-desc
#  33. statistics-fail-all
#  34. statistics-failure
#  35. test-set-bundled
#  36. ttfv-fail-all
#  37. ttfv-query-success
#  38. update-missing-wikibase-sparql
#  39. update-software-data
#  40. update-wikibase-primary-language-3
#  41. update-wikibase-primary-language-4
#  42. user-2000
#  43. user-fail-all
#  44. connectivity-success-complex
#  45. external-identifier-success
#  46. log-first-failure
#  47. log-last-failure
#  48. merge-software-by-id
#  49. property-popularity-success
#  50. quantity-success
#  51. recent-changes-success-ood
#  52. software-version-success
#  53. software-version-success-ii
#  54. statistics-success
#  55. ttfv-success
#  56. update-missing-wikibase-script-path
#  57. update-wikibase-primary-language-2
#  58. update-wikibase-type-other
#  59. update-wikibase-type-suite
#  60. update-wikibase-type-test
#  61. user-20
#  62. add-test-software
#  63. add-wikibase-ii
#  64. cloud-wikibase-set-reuse-true
#  65. connectivity-success-simple-5
#  66. external-identifier-success-ood
#  67. log-first-success-1
#  68. log-last-success-1
#  69. property-popularity-success-ood
#  70. quantity-success-ood
#  71. software-version-fail-ood
#  72. statistics-fail-ood
#  73. ttfv-fail-ood
#  74. update-wikibase-primary-language-1
#  75. user-failure
#  76. log-first-success-ood
#  77. log-last-success-ood
#  78. mutate-cloud-instances
#  79. remove-wikibase-language-2
#  80. update-wikibase-url
#  81. user-empty-ood
#  82. add-wikibase-language-2
#  83. add-wikibase-script-path
#  84. query-cloud-instances
#  85. add-wikibase-language-1
#  86. wikibase-set-reuse-true
#  87. add-wikibase
#  88. wikibase-set-reuse-false
#  89. add-test-categories
#  90. transform-cloud-instance
#  91. update-cloud-instance
#  92. insert-cloud-instance

# Summary:

# Tests with dependencies: 91
# Dependency relationships: 146
