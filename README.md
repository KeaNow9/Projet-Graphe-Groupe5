# Projet Graphe - Groupe 5

Projet réalisé dans le cadre du cours **ALMF51 – Algorithmes de graphes : Parcours, optimisation et applications** à **EFREI Paris**.

## 🎯 Objectif
Développer une application permettant d’expérimenter différents algorithmes de graphes sur un réseau routier entre plusieurs villes françaises.  
Chaque algorithme sera testé sur un graphe pondéré où les sommets représentent les villes et les arêtes les routes (pondérées par la distance ou le coût).

## 🧠 Algorithmes implémentés
### Partie I – Parcours de graphe
- [x] Parcours en largeur (**BFS**)
- [x] Parcours en profondeur (**DFS**)

### Partie II – Arbre couvrant minimal
- [x] Algorithme de **Kruskal**
- [x] Algorithme de **Prim**

### Partie III – Chemins optimaux
- [x] **Dijkstra** (plus court chemin entre deux villes)
- [x] **Bellman-Ford** (gestion de poids négatifs)
- [x] **Floyd-Warshall** (tous les plus courts chemins)

## 🖥️ Structure du projet
Projet-Graphe-Groupe5/
│
├── algorithmes/                          # Module principal regroupant la logique des algorithmes
│   ├── mainTest/                         # Ancien contenu de tests
│   ├── Partie 1 (BFS, DFS)/              # ⚠️ Vide — le contenu a été déplacé dans graph.py
│   ├── Partie 2 (Kruskal Prim)/          # ⚠️ Vide — déplacé dans graph.py
│   ├── Partie 3 (Dijkstra)/              # ⚠️ Vide — déplacé dans graph.py
│   ├── Partie 4 (Bellman-Ford, Floyd-Warshall)/   # ⚠️ Vide — déplacé dans graph.py
│   └── Partie_generale/
│       ├── __init__.py
│       └── graph.py                      # ✅ Contient désormais l’ensemble des algorithmes
│
├── flask_d3_graph_app/                   # Application Flask + visualisation D3.js
│   └── flask_d3_graph_app/
│       ├── static/                       # Ressources statiques (styles, JS…)
│       │   ├── css/                      # Feuilles de styles
│       │   └── js/                       # Scripts JavaScript
│       │
│       ├── templates/                    # Templates HTML utilisés par Flask
│       │   └── index.html                # Page principale affichant le graphe
│       │
│       ├── algorithms.py                 # Interface entre Flask et graph.py
│       ├── app.py                        # Point d’entrée de l’application Flask
│       ├── requirements.txt              # Dépendances nécessaires à l’interface
│       └── README.md                     # Instructions pour lancer l’interface web
│
├── .gitignore                            # Fichiers/dossiers exclus du versionnage
├── main.py                               # Launcher / script général
├── README.md                             # ✅ README principal (celui-ci)
└── requirements.txt                      # Dépendances générales (tests des algorithmes)





## 🚀 Utilisation de l’interface web

> ⚠️ Les instructions détaillées pour lancer l’application Flask se trouvent dans :  
➡️ `flask_d3_graph_app/flask_d3_graph_app/README.md`

Ce fichier explique :
✅ création d’un environnement virtuel  
✅ installation des dépendances  
✅ lancement de `app.py`  

---

## 🛠 Technologies utilisées

- Python
- Flask
- D3.js
- HTML / CSS / JS

---

## 👥 Membres du groupe

- *Ornella MOTENGO BAUTI*
- *Charles MATOU KAMGA*
- *Yanni MAMECHE*
- *Keanu TAUHIRO*

---

## ✅ Résumé

- Tous les algorithmes sont centralisés dans `graph.py`
- Une interface Flask permet leur visualisation/exécution
- Le README interne (`flask_d3_graph_app/.../README.md`) contient les consignes pour lancer l’application

---