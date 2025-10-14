from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable, Optional

@dataclass(frozen=True)
class Arete:
    """Représente une arête pondérée entre deux sommets."""
    u: str  # Sommet de départ
    v: str  # Sommet d’arrivée
    w: float = 1.0  # Poids de l’arête (distance, coût, etc.)

class Graphe:
    """
    Classe représentant un graphe pondéré.
    Par défaut, le graphe est non orienté (routes à double sens).
    Si directed=True, les arêtes auront un sens (orienté).
    """

    def __init__(self, oriente: bool = False) -> None:
        self.oriente = oriente
        # Dictionnaire d’adjacence : {sommet: {voisin: poids}}
        self._adj: Dict[str, Dict[str, float]] = {}

    # ---- Construction du graphe ----
    def ajouter_sommet(self, u: str) -> None:
        """Ajoute un sommet au graphe s’il n’existe pas déjà."""
        self._adj.setdefault(u, {})

    def ajouter_arete(self, u: str, v: str, w: float = 1.0) -> None:
        """
        Ajoute une arête pondérée entre deux sommets.
        Si le graphe n’est pas orienté, ajoute aussi l’arête inverse.
        """
        self.ajouter_sommet(u)
        self.ajouter_sommet(v)
        self._adj[u][v] = w
        if not self.oriente:
            self._adj[v][u] = w

    # ---- Accès aux données ----
    def sommets(self) -> List[str]:
        """Retourne la liste des sommets du graphe."""
        return list(self._adj.keys())

    def aretes(self) -> List[Arete]:
        """
        Retourne la liste de toutes les arêtes sous forme d’objets Arete.
        Pour un graphe non orienté, les doublons sont évités.
        """
        deja_vu = set()
        A: List[Arete] = []
        for u, voisins in self._adj.items():
            for v, w in voisins.items():
                if self.oriente or ((u, v) not in deja_vu and (v, u) not in deja_vu):
                    A.append(Arete(u, v, w))
                    deja_vu.add((u, v))
        return A

    def voisins(self, u: str) -> Iterable[Tuple[str, float]]:
        """Retourne les voisins d’un sommet et le poids des arêtes correspondantes."""
        return self._adj.get(u, {}).items()

    def poids(self, u: str, v: str) -> Optional[float]:
        """Retourne le poids de l’arête entre deux sommets (None si elle n’existe pas)."""
        return self._adj.get(u, {}).get(v)

    # ---- Méthodes utilitaires ----
    @classmethod
    def depuis_liste_aretes(
        cls, aretes: Iterable[Tuple[str, str, float]], oriente: bool = False
    ) -> "Graphe":
        """
        Crée un graphe à partir d’une liste d’arêtes (u, v, w).
        Exemple :
            G = Graphe.depuis_liste_aretes([
                ("Paris", "Lyon", 465),
                ("Paris", "Caen", 50)
            ])
        """
        g = cls(oriente=oriente)
        for u, v, w in aretes:
            g.ajouter_arete(u, v, w)
        return g
