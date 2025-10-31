# algorithms.py
# ===========================================================
# Contient ta classe Graph + les fonctions appelées par Flask
# ===========================================================

from typing import List, Dict, Tuple
from collections import defaultdict
import math
import networkx as nx

# ===========================================================
# Classe Graph avec tes algorithmes
# ===========================================================

class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.edges = []
        self.directed = directed

    def add_edge(self, u, v, w=1):
        self.graph[u].append((v, w))
        self.edges.append((w, u, v))
        if not self.directed:
            self.graph[v].append((u, w))
            self.edges.append((w, v, u))

    def get_nodes(self):
        return list(self.graph.keys())

    # ----------------------
    # BFS
    # ----------------------
    def bfs(self, start):
        visited = set()
        queue = [start]
        order = []
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor, _ in self.graph[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return order

    # ----------------------
    # DFS
    # ----------------------
    def dfs(self, start):
        visited = set()
        order = []

        def explore(node):
            visited.add(node)
            order.append(node)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    explore(neighbor)

        explore(start)
        return order

    # ----------------------
    # Kruskal
    # ----------------------
    def kruskal(self):
        if self.directed:
            raise ValueError("Kruskal ne s'applique qu'aux graphes non orientés !")
        parent = {n: n for n in self.graph}

        def find(n):
            while parent[n] != n:
                n = parent[n]
            return n

        acpm, total = [], 0
        for w, u, v in sorted(self.edges):
            if find(u) != find(v):
                parent[find(v)] = find(u)
                acpm.append((u, v, w))
                total += w
        return acpm, total

    # ----------------------
    # Prim
    # ----------------------
    def prim(self, start):
        if self.directed:
            raise ValueError("Prim ne peut être utilisé que sur un graphe non orienté !")
        sommets_visites = set([start])
        aretes = [(w, start, v) for v, w in self.graph[start]]
        acpm = []
        cout_total = 0
        while aretes:
            min_index = 0
            for i in range(len(aretes)):
                if aretes[i][0] < aretes[min_index][0]:
                    min_index = i
            w, u, v = aretes.pop(min_index)
            if v not in sommets_visites:
                sommets_visites.add(v)
                acpm.append((u, v, w))
                cout_total += w
                for to, weight in self.graph[v]:
                    if to not in sommets_visites:
                        aretes.append((weight, v, to))
        return acpm, cout_total

    # ----------------------
    # Dijkstra
    # ----------------------
    def dijkstra(self, start):
        dist = {node: math.inf for node in self.graph}
        dist[start] = 0
        visited = set()
        while len(visited) < len(self.graph):
            min_node = None
            min_dist = math.inf
            for node in self.graph:
                if node not in visited and dist[node] < min_dist:
                    min_dist = dist[node]
                    min_node = node
            if min_node is None:
                break
            visited.add(min_node)
            for neighbor, weight in self.graph[min_node]:
                if neighbor not in visited:
                    new_dist = dist[min_node] + weight
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
        return dist

    # ----------------------
    # Bellman-Ford
    # ----------------------
    def bellman_ford(self, start):
        dist = {node: math.inf for node in self.graph}
        dist[start] = 0
        for _ in range(len(self.graph) - 1):
            for w, u, v in self.edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        for w, u, v in self.edges:
            if dist[u] + w < dist[v]:
                return None
        return dist

    # ----------------------
    # Floyd-Warshall
    # ----------------------
    def floyd_warshall(self):
        nodes = list(self.graph.keys())
        dist = {i: {j: math.inf for j in nodes} for i in nodes}
        for node in nodes:
            dist[node][node] = 0
            for neighbor, w in self.graph[node]:
                dist[node][neighbor] = w
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist


# ===========================================================
# Wrappers pour le frontend Flask/D3
# ===========================================================

def _nx_to_user_graph(G: nx.Graph) -> Graph:
    directed = isinstance(G, nx.DiGraph)
    UG = Graph(directed=directed)
    for u, v, d in G.edges(data=True):
        w = float(d.get("weight", 1.0))
        UG.add_edge(str(u), str(v), w)
    return UG

def _user_to_nx(UG: Graph) -> nx.Graph:
    H = nx.DiGraph() if UG.directed else nx.Graph()
    for u, neighs in UG.graph.items():
        for v, w in neighs:
            H.add_edge(u, v, weight=float(w))
    return H


def _reconstruct_path_from_dist(UG: Graph, dist: Dict[str, float], source: str, target: str) -> List[str]:
    if source not in dist or target not in dist or math.isinf(dist[target]):
        return []
    current = target
    path = [current]
    seen = set([current])
    for _ in range(len(UG.graph) + 5):
        if current == source:
            return list(reversed(path))
        found_prev = None
        for u, neighs in UG.graph.items():
            for v, w in neighs:
                if v == current:
                    if u in dist and not math.isinf(dist[u]) and abs(dist[u] + w - dist[v]) < 1e-9:
                        if (found_prev is None) or (dist[u] < dist[found_prev]):
                            found_prev = u
        if found_prev is None or found_prev in seen:
            break
        current = found_prev
        path.append(current)
        seen.add(current)
    return []


# ===========================================================
# Fonctions appelées par l'interface web
# ===========================================================

def bfs(G: nx.Graph, source: str) -> List[str]:
    UG = _nx_to_user_graph(G)
    return UG.bfs(source)

def dfs(G: nx.Graph, source: str) -> List[str]:
    UG = _nx_to_user_graph(G)
    return UG.dfs(source)

def dijkstra(G: nx.Graph, source: str, target: str) -> Tuple[List[str], float]:
    UG = _nx_to_user_graph(G)
    # 1) calcule les distances avec ton Dijkstra maison
    dist = UG.dijkstra(source)

    # si source/target invalides ou unreachable
    if not dist or target not in dist or math.isinf(dist[target]):
        return [], float("inf")

    # 2) essaie la reconstruction sur la base des distances
    path = _reconstruct_path_from_dist(UG, dist, source, target)

    # 3) SECURITÉ/FALLBACK : si la reconstruction échoue, on prend un chemin sûr
    if not path:
        H = _user_to_nx(UG)
        try:
            path = nx.shortest_path(H, source=source, target=target, weight="weight")
        except Exception:
            path = []

    return path, float(dist[target])


def kruskal(G: nx.Graph) -> Tuple[List[Tuple[str, str, float]], float]:
    UG = _nx_to_user_graph(G)
    mst, total = UG.kruskal()
    edges = [(str(u), str(v), float(w)) for (u, v, w) in mst]
    return edges, float(total)

def prim(G: nx.Graph, start: str) -> Tuple[List[Tuple[str, str, float]], float]:
    UG = _nx_to_user_graph(G)
    mst, total = UG.prim(start)
    edges = [(str(u), str(v), float(w)) for (u, v, w) in mst]
    return edges, float(total)

def bellman_ford(G: nx.Graph, source: str) -> Dict[str, float]:
    UG = _nx_to_user_graph(G)
    dist = UG.bellman_ford(source)
    if dist is None:
        return {"__negative_cycle__": 1.0}
    return {str(k): (float(v) if not math.isinf(v) else float("inf")) for k, v in dist.items()}

def floyd_warshall_all_pairs(G: nx.Graph) -> Dict[str, Dict[str, float]]:
    UG = _nx_to_user_graph(G)
    dist = UG.floyd_warshall()
    return {str(i): {str(j): (float(d) if not math.isinf(d) else float("inf")) for j, d in row.items()} for i, row in dist.items()}
