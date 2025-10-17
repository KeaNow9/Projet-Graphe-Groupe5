from collections import defaultdict
import math

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

    def display(self):
        for node, neighbors in self.graph.items():
            print(f"{node} -> {neighbors}")

    # ----------------------
    # BFS
    # ----------------------
    def bfs(self, start):
        visited = set()  # Pour mémoriser les sommets déjà visités
        queue = [start]  # File d'attente (FIFO) avec le sommet de départ
        order = []  # Ordre de visite des sommets

        while queue:  # Tant que la file n'est pas vide
            node = queue.pop(0)  # Retirer le premier élément (comme une file)
            if node not in visited:
                visited.add(node)  # Marquer comme visité
                order.append(node)  # Ajouter à l'ordre de parcours
                for neighbor, _ in self.graph[node]:  # Parcourir ses voisins
                    if neighbor not in visited:
                        queue.append(neighbor)  # Ajouter les voisins à la file
        return order

    # ----------------------
    # DFS
    # ----------------------
    def dfs(self, start):
        visited = set()  # Pour mémoriser les sommets déjà visités
        order = []  # Ordre de visite

        def explore(node):
            visited.add(node)  # Marquer comme visité
            order.append(node)  # Enregistrer l'ordre
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    explore(neighbor)  # Appel récursif

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

        mst, total = [], 0
        for w, u, v in sorted(self.edges):  # tri automatique par le poids
            if find(u) != find(v):
                parent[find(v)] = find(u)
                mst.append((u, v, w))
                total += w
        return mst, total

    # ----------------------
    # Prim
    # ----------------------
    def prim(self, start):
        if self.directed:
            raise ValueError("Prim ne peut être utilisé que sur un graphe non orienté !")

        visited = set([start])
        edges = [(w, start, v) for v, w in self.graph[start]]
        mst = []
        total_cost = 0

        while edges:
            # trouve l'arête de poids minimal
            min_index = 0
            for i in range(len(edges)):
                if edges[i][0] < edges[min_index][0]:
                    min_index = i
            w, u, v = edges.pop(min_index)

            if v not in visited:
                visited.add(v)
                mst.append((u, v, w))
                total_cost += w
                for to, weight in self.graph[v]:
                    if to not in visited:
                        edges.append((weight, v, to))

        return mst, total_cost

    # ----------------------
    # Dijkstra
    # ----------------------
    def dijkstra(self, start):
        print(f"\n=== Algorithme de Dijkstra (depuis {start}) ===")
        # Initialisation
        dist = {node: math.inf for node in self.graph}
        dist[start] = 0
        visited = set()
        while len(visited) < len(self.graph):
            # Trouver le nœud non visité avec la plus petite distance
            min_node = None
            min_dist = math.inf
            for node in self.graph:
                if node not in visited and dist[node] < min_dist:
                    min_dist = dist[node]
                    min_node = node

            if min_node is None:
                break  # Tous les nœuds atteignables ont été visités

            # Marquer le nœud comme visité
            visited.add(min_node)

            # Mettre à jour les distances des voisins
            for neighbor, weight in self.graph[min_node]:
                if neighbor not in visited:
                    new_dist = dist[min_node] + weight
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist

        # Affichage des résultats
        for node in dist:
            d = "∞" if dist[node] == math.inf else dist[node]
            print(f"Distance minimale de {start} à {node} = {d}")

        return dist

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

    # ----------------------
    # Affichage graphique du graphe
    # ----------------------
    def afficher_graphe_graphique(self):
        import networkx as nx
        import matplotlib.pyplot as plt
        # Création du graphe NetworkX
        G = nx.Graph() if not self.directed else nx.DiGraph()
        # Ajout des arêtes et des poids
        for u in self.graph:
            for v, w in self.graph[u]:
                G.add_edge(u, v, weight=w)
        # Position automatique des sommets
        pos = nx.spring_layout(G, seed=42)  # disposition harmonieuse
        # Dessin du graphe
        plt.figure(figsize=(10, 7))
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1200, edgecolors='black')
        nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        # Poids des arêtes
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=9)
        plt.title("Réseau routier des villes", fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.show()

    # --------------------------------------------------------
    # Exemple d’utilisation
    # --------------------------------------------------------
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



        # --- Démonstrations identiques à ton exemple ---
        print("=== Parcours ===")
        print("BFS depuis Rennes :", g.bfs("Rennes"))
        print("DFS depuis Rennes :", g.dfs("Rennes"))

        print("\n=== Arbre couvrant minimal ===")
        mst_k, cost_k = g.kruskal()
        print("Kruskal :", mst_k, " | Coût total :", cost_k)

        mst_p, cost_p = g.prim("Rennes")
        print("Prim :", mst_p, " | Coût total :", cost_p)

        print("\n=== Plus courts chemins ===")
        print("Dijkstra (depuis Bordeaux) :", g.dijkstra("Bordeaux"))
        print("Bellman-Ford (depuis Bordeaux) :", g.bellman_ford("Bordeaux"))

        print("\n=== Floyd-Warshall ===")
        dist = g.floyd_warshall()
        for i in dist:
            print(i, dist[i])

        g.afficher_graphe_graphique()