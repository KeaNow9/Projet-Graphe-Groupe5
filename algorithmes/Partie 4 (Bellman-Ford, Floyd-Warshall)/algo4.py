from algorithmes.Partie_generale.graph2 import Graph
import math

#from networkx.classes import Graph

# ==============================================
#  Algorithmes de plus courts chemins :
#  - Bellman-Ford (depuis un seul sommet)
#  - Floyd-Warshall (toutes les paires de sommets)
# ==============================================


# ----------------------
# Bellman-Ford
# ----------------------
def bellman_ford(self, start):
    # Initialisation : toutes les distances à l'infini
    dist = {node: math.inf for node in self.graph}
    # La distance du sommet de départ à lui-même est 0
    dist[start] = 0

    # Étape 1 : Relaxation des arêtes |V| - 1 fois
    # (où |V| = nombre de sommets)
    for _ in range(len(self.graph) - 1):
        for w, u, v in self.edges:
            # Si le chemin passant par u vers v est plus court, on met à jour
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Étape 2 : Détection de cycle de poids négatif
    # Si une relaxation est encore possible, il y a un cycle négatif
    for w, u, v in self.edges:
        if dist[u] + w < dist[v]:
            print("Cycle négatif détecté !")
            return None

    # Retourne les distances minimales depuis le sommet de départ
    return dist


# ----------------------
# Floyd-Warshall
# ----------------------
def floyd_warshall(self):
    # Liste de tous les sommets du graphe
    nodes = list(self.graph.keys())

    # Initialisation de la matrice des distances
    # dist[i][j] = distance minimale connue de i à j
    dist = {i: {j: math.inf for j in nodes} for i in nodes}

    # Distance nulle pour les boucles (de i à i)
    # et initialisation des distances directes (arêtes existantes)
    for node in nodes:
        dist[node][node] = 0
        for neighbor, w in self.graph[node]:
            dist[node][neighbor] = w

    # Triple boucle : programmation dynamique
    # On teste si passer par un sommet intermédiaire k améliore le chemin i -> j
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Retourne la matrice complète des plus courts chemins
    return dist


# =======================================================
#          Programme principal pour tester les algos
# =======================================================

if __name__ == "__main__":
        g = Graph(directed=False)

        # --- Arêtes d'après le schéma ---
        # Rennes
        g.add_edge("Rennes", "Nantes", 45)
        g.add_edge("Rennes", "Caen", 75)
        g.add_edge("Rennes", "Paris", 110)
        g.add_edge("Rennes", "Bordeaux", 130)

        # Nantes
        g.add_edge("Nantes", "Paris", 80)
        g.add_edge("Nantes", "Bordeaux", 90)

        # Bordeaux
        g.add_edge("Bordeaux", "Paris", 150)
        g.add_edge("Bordeaux", "Lyon", 100)

        # Caen
        g.add_edge("Caen", "Paris", 50)
        g.add_edge("Caen", "Lille", 65)

        # Paris
        g.add_edge("Paris", "Lille", 70)
        g.add_edge("Paris", "Dijon", 60)

        # Lille
        g.add_edge("Lille", "Dijon", 120)
        g.add_edge("Lille", "Nancy", 100)

        # Dijon
        g.add_edge("Dijon", "Nancy", 75)
        g.add_edge("Dijon", "Lyon", 70)
        g.add_edge("Dijon", "Grenoble", 75)

        # Lyon
        g.add_edge("Lyon", "Grenoble", 40)
        g.add_edge("Lyon", "Nancy", 90)

        # Nancy
        g.add_edge("Nancy", "Grenoble", 80)

        g.afficher_graphe_graphique()

        print("Bellman-Ford (depuis Bordeaux) :", g.bellman_ford("Bordeaux"))

        print("\n=== Floyd-Warshall ===")
        dist = g.floyd_warshall()
        for i in dist:
            print(i, dist[i])