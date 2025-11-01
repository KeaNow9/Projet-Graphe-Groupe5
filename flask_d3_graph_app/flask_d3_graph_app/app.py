import os
from flask import Flask, jsonify, request, render_template
import networkx as nx
from algorithms import bfs, dfs, dijkstra, kruskal, prim, bellman_ford, floyd_warshall_all_pairs

app = Flask(__name__)

# ---------- Déclaration de 2 graphes ----------
def make_fr_routes():
    G = nx.Graph()
    edges = [
        ("Rennes", "Nantes", 45), ("Rennes", "Caen", 75),
        ("Rennes", "Paris", 110), ("Rennes", "Bordeaux", 130),
        ("Nantes", "Paris", 80),  ("Nantes", "Bordeaux", 90),
        ("Bordeaux", "Paris", 150), ("Bordeaux", "Lyon", 100),
        ("Caen", "Paris", 50), ("Caen", "Lille", 65),
        ("Paris", "Lille", 70), ("Paris", "Dijon", 60),
        ("Lille", "Dijon", 120), ("Lille", "Nancy", 100),
        ("Dijon", "Nancy", 75), ("Dijon", "Lyon", 70), ("Dijon", "Grenoble", 75),
        ("Lyon", "Grenoble", 40), ("Lyon", "Nancy", 90),
        ("Nancy", "Grenoble", 80),
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G, "Paris"  # source fixée pour ce graphe

def make_neg_demo():
    # petit graphe orienté pour Bellman-Ford
    G = nx.DiGraph()
    edges = [
        ("A","B",4), ("A","C",2), ("B","C",-1), ("B","D",2),
        ("C","D",3), ("C","E",-2), ("E","D",1)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G, "A"      # source fixée ici

GRAPHS = {
    "fr_routes": {
        "graph": make_fr_routes()[0],
        "default_source": make_fr_routes()[1]
    },
    "demo_small": {
        "graph": make_neg_demo()[0],
        "default_source": make_neg_demo()[1]
    },
}


def get_graph(name: str):
    return GRAPHS.get(name) or GRAPHS["fr_routes"]

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/graph")
def api_graph():
    name = request.args.get("name", "fr_routes")  # <-- récupère ?name= depuis l’URL
    print(">>> Graphe demandé :", name)

    pack = get_graph(name)                       # <-- récupère le bon graphe selon ce nom
    G = pack["graph"]
    print("Graph directed ?", G.is_directed())

    nodes = [{"id": str(n)} for n in G.nodes()]
    links = [
        {"source": str(u), "target": str(v), "weight": float(d.get("weight", 1.0))}
        for u, v, d in G.edges(data=True)
    ]

    return jsonify({
        "name": name,
        "defaultSource": pack["default_source"],
        "nodes": nodes,
        "links": links,
        "directed": G.is_directed()
    })


@app.post("/api/run")
def api_run():
    data = request.get_json(force=True)
    name = data.get("graph", "fr_routes")
    pack = get_graph(name)
    G = pack["graph"]

    # ✅ PRENDRE la source envoyée par l’UI si présente, sinon la valeur par défaut
    source = data.get("source") or pack["default_source"]

    # ✅ Validation : la source doit exister dans le graphe
    if source not in G:
        return jsonify({"error": f"Source inconnue: {source}"}), 400

    target = data.get("target")
    algo = data.get("algo")
    result = {}

    if algo == "bfs":
        order = bfs(G, source)
        result = {"order": order, "nodes_to_highlight": order}

    elif algo == "dfs":
        order = dfs(G, source)
        result = {"order": order, "nodes_to_highlight": order}

    elif algo == "dijkstra":
        if not target:
            return jsonify({"error": "Cible manquante"}), 400
        if target not in G:
            return jsonify({"error": f"Cible inconnue: {target}"}), 400
        path, cost = dijkstra(G, source, target)
        edges_on_path = [{"source": path[i], "target": path[i+1]} for i in range(len(path)-1)] if len(path) > 1 else []
        result = {"path": path, "cost": cost, "edges_to_highlight": edges_on_path, "nodes_to_highlight": path}

    elif algo == "kruskal":
        mst_edges, total = kruskal(G)
        edges_fmt = [{"source": u, "target": v} for u, v, _ in mst_edges]
        result = {"tree_edges": edges_fmt, "total": total, "edges_to_highlight": edges_fmt}

    elif algo == "prim":
        mst_edges, total = prim(G, source)   # ✅ utilise la source choisie
        edges_fmt = [{"source": u, "target": v} for u, v, _ in mst_edges]
        result = {"tree_edges": edges_fmt, "total": total, "edges_to_highlight": edges_fmt}


    elif algo == "bellman":
        table = bellman_ford(G, source)  # ⚡ renvoie {"table": [...]}
        if isinstance(table, dict) and "__negative_cycle__" in table:
            return jsonify({"error": "Cycle négatif détecté"}), 400
        result = {
            "table": table["table"],  # envoie directement le tableau
            "nodes_to_highlight": [source]  # met en évidence la source
        }

    elif algo == "floyd":
        dist = floyd_warshall_all_pairs(G)
        result = {"distances": dist}

    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

