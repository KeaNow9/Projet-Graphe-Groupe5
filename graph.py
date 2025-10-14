from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable, Optional

@dataclass(frozen=True)
class Edge:
    u: str
    v: str
    w: float = 1.0

class Graph:
    """Graphe pondéré non orienté par défaut (roads). Orienté si directed=True."""
    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._adj: Dict[str, Dict[str, float]] = {}

    # ---- construction
    def add_node(self, u: str) -> None:
        self._adj.setdefault(u, {})

    def add_edge(self, u: str, v: str, w: float = 1.0) -> None:
        self.add_node(u); self.add_node(v)
        self._adj[u][v] = w
        if not self.directed:
            self._adj[v][u] = w

    # ---- accès
    def nodes(self) -> List[str]:
        return list(self._adj.keys())

    def edges(self) -> List[Edge]:
        seen = set()
        E: List[Edge] = []
        for u, nbrs in self._adj.items():
            for v, w in nbrs.items():
                if self.directed or (u, v) not in seen and (v, u) not in seen:
                    E.append(Edge(u, v, w))
                    seen.add((u, v))
        return E

    def neighbors(self, u: str) -> Iterable[Tuple[str, float]]:
        return self._adj.get(u, {}).items()

    def weight(self, u: str, v: str) -> Optional[float]:
        return self._adj.get(u, {}).get(v)

    # ---- utilitaires
    @classmethod
    def from_edge_list(cls, edges: Iterable[Tuple[str, str, float]], directed: bool = False) -> "Graph":
        g = cls(directed=directed)
        for u, v, w in edges:
            g.add_edge(u, v, w)
        return g
