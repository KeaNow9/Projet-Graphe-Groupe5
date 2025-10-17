def kruskal(self):
    if self.directed:
        raise ValueError("Kruskal ne s'applique qu'aux graphes non orientés !")

    parent = {n: n for n in self.graph}

    def find(n):
        while parent[n] != n:
            n = parent[n]
        return n

    mst, total = [], 0
    for w, u, v in sorted(self.edges):  # tri automatique par le poids
        if find(u) != find(v):
            parent[find(v)] = find(u)
            mst.append((u, v, w))
            total += w

    return mst, total
