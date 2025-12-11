from tarjan import tarjan_recursive


def topological_sort(dependency_pairs):
    "Sort values subject to dependency constraints"
    nodes = {}
    for e in dependency_pairs:
        if e.di not in nodes:
            nodes[e.di] = []
        if e.si not in nodes:
            nodes[e.si] = []
        if e.di not in nodes[e.si]:
            nodes[e.si].append(e.di)
    out = tarjan_recursive(nodes)
    return out
