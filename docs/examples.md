# Exemples

Tous les exemples se trouvent dans le dossier `examples/`. Lancez-les avec :

```bash
python examples/01_hello.py
```

## Exemples disponibles

| Fichier | Contenu |
|---------|---------|
| `01_hello.py` | Fenêtre simple, composants de base, bascule de thème |
| `03_app_shell.py` | Application de gestion : Sidebar + Navbar + pages + routes |
| `04_forms.py` | Formulaire complet avec validation et soumission |
| `05_table.py` | DataTable : tri, recherche, pagination, export CSV, menu contextuel |
| `06_gest_clients.py` | Application de gestion de clients complète (tutoriel) |
| `07_dashboard.py` | Dashboard : StatCards, graphique, activités, timeline, onglets, badges |
| `08_state.py` | État réactif : compteur lié via bind_state, thème piloté par l'état |

## Code minimal

```python
from pyui import App

app = App(title="Mon application")
app.run()
```

## Code de démonstration complet

Le tutoriel (docs/tutorial.md) construit pas à pas une application de gestion
de clients. Son code complet est dans `examples/06_gest_clients.py`.