# PyUI

![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?logo=python)
![License MIT](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.1.0-0A8?logo=python)
![Tests](https://img.shields.io/badge/tests-110%20passed-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-77%25-yellow)
![PyPI](https://img.shields.io/pypi/v/pyui-gui)
![CI](https://github.com/NockiProgramTECH/pyui/actions/workflows/ci.yml/badge.svg)

**PyUI** — Framework GUI desktop Python au-dessus de Tkinter/ttk.

Construisez des logiciels desktop professionnels rapidement avec une API
explicite, un design system réactif (clair/sombre), des layouts déclaratifs, des
formulaires validés, un DataTable triable/paginé, une navigation avec historique,
des notifications toast et un Dashboard intégré — **sans `**kwargs`** dans les
signatures publiques.

---

## Démarrage rapide

```python
from pyui import App, Button, Label, Column

app = App(title="Gestion", size=(1000, 700))

col = Column(app, spacing=8)
col.pack(fill="both", expand=True, padx=16, pady=16)

Label(col, text="Bienvenue", size="2xl", weight="bold")
Button(col, text="OK", variant="primary", command=app.close)

app.run()
```

## Nouveautés 0.1.0

- **Placement modélisé** (`pack`/`grid`/`place`) : chaque paramètre est nommé,
  typé et validé — plus de `**kwargs`
- **50+ composants** : Button, Card, DataTable, Form, Sidebar, Tabs, Chart,
  Toast, Modal, Dashboard, Spinner, Accordion, Badge, Alert…
- **Design System** complet avec mode clair/sombre, typographie, espacements
- **État réactif** : `State` + `Component.bind_state()` pour des composants
  qui se mettent à jour automatiquement
- **8 exemples** d'application, du hello-world au dashboard complet
- **110 tests** unitaires (77 % de couverture)
- **16 fichiers** de documentation structurée + tutoriel pas à pas

## Documentation

[Documentation complète](docs/index.md) | [Démarrage rapide](docs/quickstart.md) |
[Tutoriel](docs/tutorial.md) | [Composants](docs/components.md) |
[Placement](docs/placement.md) | [Formulaires](docs/forms.md) |
[DataTable](docs/tables.md) | [Navigation](docs/navigation.md) |
[Thème](docs/theme.md) | [Référence API](docs/api_reference.md) |
[Exemples](docs/examples.md)

## Exemples

```bash
python examples/01_hello.py          # Fenêtre simple
python examples/03_app_shell.py      # Sidebar + Navbar
python examples/04_forms.py          # Formulaires + validation
python examples/05_table.py          # DataTable : tri, recherche, export
python examples/06_gest_clients.py   # App de gestion complète (tutoriel)
python examples/07_dashboard.py      # Dashboard avec graphique
python examples/08_state.py          # État réactif
```

## Installation

```bash
# Développement
pip install -e ".[dev]"

# Depuis un wheel (construit)
pip install dist/pyui_gui-0.1.0-py3-none-any.whl

# Depuis PyPI
pip install pyui-gui
```

## Contribuer

1. Forker le projet
2. Créer une branche (`git checkout -b feature/ma-idee`)
3. Commiter (`git commit -am 'Ajoute une fonctionnalite'`)
4. Pusher (`git push origin feature/ma-idee`)
5. Ouvrir une Pull Request

## Licence

MIT — © 2026 PyUI

---

*Propulsé par Tkinter/ttk — Python 3.9+ requis.*