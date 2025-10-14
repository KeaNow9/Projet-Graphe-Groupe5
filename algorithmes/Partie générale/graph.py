from collections import defaultdict

class Graphe:
    def __init__(self, oriente=False):
        """
        Initialise un graphe vide.
        :param oriente: True si le graphe est orienté, False sinon.
        """
        self.graphe = defaultdict(list)  # Liste d’adjacence
        self.aretes = []  # Liste d’arêtes (utile pour Kruskal / Bellman-Ford)
        self.oriente = oriente

    def ajouter_arete(self, u, v, poids=1):
        """
        Ajoute une arête entre u et v avec un poids.
        """
        self.graphe[u].append((v, poids))
        self.aretes.append((poids, u, v))
        if not self.oriente:
            self.graphe[v].append((u, poids))
            self.aretes.append((poids, v, u))

    def sommets(self):
        """Renvoie la liste des sommets du graphe."""
        return list(self.graphe.keys())

    def afficher(self):
        """Affiche la liste d’adjacence du graphe."""
        for sommet, voisins in self.graphe.items():
            print(f"{sommet} -> {voisins}")
