# Layouts

> **Placement** : pour positionner un widget directement (`pack`, `grid`, `place`)
> avec tous les paramètres listés, voir [placement.md](placement.md).

## `Container`

Zone de contenu avec padding, s'étire par défaut.

```python
Container(parent, padding=16, fill=True, expand=True)
```

## `Row`

Place les enfants horizontalement.

```python
row = Row(parent, spacing=8)
Button(row, text="A")
Button(row, text="B")
# Variante fluide : row.add(Button, text="C").add(Button, text="D")
```

`row.add(Classe, **params)` crée le composant avec `params` = ses paramètres de
constructeur (tous listés dans [components.md](components.md)).

## `Column`

Place les enfants verticalement (étirés par défaut).

```python
col = Column(parent, spacing=8)
Label(col, text="Nom")
Input(col, placeholder="Votre nom")
```

## `Stack`

Alias de `Column` (empilement vertical).

## `Grid`

Grille régulière à colonnes uniformes.

```python
grid = Grid(parent, columns=3, spacing=8)
grid.add(Card, title="A").add(Card, title="B").add(Card, title="C")
```

## `Sidebar`

Menu latéral avec icônes, éléments actifs, sous-menus et navigation intégrée.

```python
Sidebar(
    parent,
    title="Menu",
    logo="▦",
    width=240,
    position="left",
    items=[
        {"key": "dashboard", "text": "Dashboard", "icon": "home", "route": "/"},
        {"text": "Ventes", "icon": "chart", "children": [
            {"key": "nv", "text": "Nouvelle vente", "route": "/ventes/nouvelle"},
        ]},
    ],
    app=app,  # pour la navigation automatique
)
```

**Méthodes** : `set_active(key)`, `collapse(animated=False)`, `expand(animated=False)`

## `Navbar`

Barre de navigation supérieure avec titre et actions.

```python
Navbar(parent, title="Dashboard", actions=[
    {"icon": "bell", "variant": "ghost"},
    {"text": "Thème", "icon": "settings", "variant": "ghost", "command": toggle_theme},
])
```

**Méthodes** : `set_title(title)`

## `Footer`

Pied de page.

```python
Footer(parent, text="© 2026 PyUI")
```