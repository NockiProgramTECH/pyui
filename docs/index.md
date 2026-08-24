# Documentation PyUI

**PyUI** est un framework GUI desktop Python au-dessus de Tkinter/ttk. Il fournit une couche d'abstraction moderne avec des composants réutilisables, des layouts, un système de thème, des formulaires, un DataTable, une navigation intégrée et des notifications.

## Table des matières

1. [Installation](installation.md)
2. [Démarrage rapide](quickstart.md)
3. [Tutoriel : première application](tutorial.md)
4. [Composants](components.md)
5. [Placement des widgets](placement.md)
6. [Layouts](layouts.md)
7. [Formulaires](forms.md)
8. [Table de données](tables.md)
9. [Navigation](navigation.md)
10. [Thème](theme.md)
11. [Icônes](icons.md)
12. [État](state.md)
13. [Dialogue et notifications](dialogs.md)
14. [API complète](api_reference.md)
15. [Exemples](examples.md)

## Architecture

```
Application
    │
    ▼
┌────────────────────────────┐
│         PyUI API           │
├────────────────────────────┤
│ Components │ Layouts       │
│ Forms      │ Tables        │
│ Navigation │ Theme         │
│ Icons      │ Events/State  │
└──────────────┬─────────────┘
               │
               ▼
        Tkinter / ttk
               │
               ▼
             OS
```

## Package

Disponible sur PyPI :

```bash
pip install pyui-gui
```

```python
from pyui import App, Sidebar, Card, Button

app = App(title="Mon application")
app.run()
```

> Installation complète (PyPI, développement, wheel) : [installation.md](installation.md)