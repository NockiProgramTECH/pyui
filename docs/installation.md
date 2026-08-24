# Installation

## Prérequis

- Python 3.9 ou supérieur
- Tkinter (inclus avec Python sous Windows / `python3-tk` sous Linux)

## Installation depuis le dossier source

```bash
cd pyui
pip install -e .
```

## Vérification

```python
from pyui import App
print(App)
```

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