from collections import defaultdict

class Graphe:
    def __init__(self, oriente=False):
        self.graphe = defaultdict(list)
        self.aretes = []
        self.oriente = oriente

    def ajouter_arete(self, u, v, w=1):
        self.graphe[u].append((v, w))
        self.aretes.append((w, u, v))
        if not self.oriente:
            self.graphe[v].append((u, w))
            self.aretes.append((w, v, u))

    def obtenir_sommets(self):
        return list(self.graphe.keys())

    def afficher(self):
        print("Liste d’adjacence du graphe :")
        for sommet, voisins in self.graphe.items():
            liste_voisins = ", ".join([f"{v}({w})" for v, w in voisins])
            print(f"  {sommet} → {liste_voisins}")



