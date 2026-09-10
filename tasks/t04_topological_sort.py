# Task 4: Topological Sort with Cycle Detection
from typing import Dict, List

def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            if v not in in_degree:
                in_degree[v] = 0
            in_degree[v] += 1

    queue = [u for u in in_degree if in_degree[u] == 0]
    result = []

    while queue:
        u = queue.pop(0)
        result.append(u)
        for v in graph.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(result) != len(in_degree):
        raise ValueError("Cycle detected in graph: topological sort impossible")
    return result
