from collections import defaultdict
from tarjan import tarjan_recursive

nodes = {}


def topological_sort(dependency_pairs):
    "Sort values subject to dependency constraints"
    for src, tgt in dependency_pairs:
        if tgt not in nodes:
            nodes[tgt] = []
        if src not in nodes:
            nodes[src] = []
        if tgt not in nodes[src]:
            nodes[src].append(tgt)
    out = tarjan_recursive(nodes)
    return out
