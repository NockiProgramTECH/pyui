# Installation

## Prérequis

- Python 3.9 ou supérieur
- Tkinter (inclus avec Python sous Windows / `python3-tk` sous Linux)

## Depuis PyPI (recommandé)

Le package est publié sur PyPI sous le nom **`pyui-gui`**.

```bash
pip install pyui-gui
```

Vérification :

```python
from pyui import App
print(App)
```

Mettre à jour :

```bash
pip install pyui-gui --upgrade
```

Désinstaller :

```bash
pip uninstall pyui-gui
```

## En développement (depuis les sources)

Pour modifier le framework lui-même ou contribuer :

```bash
git clone https://github.com/NockiProgramTECH/pyui.git
cd pyui
pip install -e ".[dev]"
```

L'installation éditable (`-e`) reflète instantanément vos modifications.

## Depuis un wheel construit

```bash
python -m build                       # génère dist/pyui_gui-0.1.1-py3-none-any.whl
pip install dist/pyui_gui-0.1.1-py3-none-any.whl
```

## Liens

- PyPI : <https://pypi.org/project/pyui-gui>
- Dépôt : <https://github.com/NockiProgramTECH/pyui>
- Documentation en ligne : <https://NockiProgramTECH.github.io/pyui>

## Structure du projet

```
pyui/
├── src/pyui/
│   ├── core/          App, Component, Page, State, Events, Router, Utils
│   ├── widgets/       Button, Label, Input, Toggle, Card, Badge, Tabs...
│   ├── layouts/       Container, Row, Column, Grid, Sidebar, Navbar, Footer
│   ├── forms/         Form, TextField, EmailField, NumberField, SelectField...
│   ├── tables/        DataTable, Column, Filter, Pagination
│   ├── theme/         Theme, colors, typography, spacing
│   ├── icons/         IconManager, GLYPHS
│   ├── dialogs/       Dialog.confirm, error, success, warning
│   └── notifications/ Toast.success, error, warning, info
├── examples/          Exemples d'application
├── tests/             Tests unitaires
└── docs/              Documentation
```
