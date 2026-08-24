# Démarrage rapide

> **Avant tout** : installer le framework → `pip install pyui-gui`
> (voir [installation](installation.md) pour les autres méthodes).

## Fenêtre minimale

```python
from pyui import App

app = App(title="Mon application")
app.run()
```

## Avec des composants

```python
from pyui import App, Button, Label, Column

app = App(title="PyUI", size=(800, 600))

col = Column(app, spacing=8)
col.pack(fill="both", expand=True, padx=24, pady=24)

Label(col, text="Bienvenue", size="2xl", weight="bold")
Label(col, text="Sous-titre", color="muted")
Button(col, text="OK", variant="primary", command=app.close)

app.run()
```

## Avec thème et layout

```python
from pyui import App, Sidebar, Navbar, Footer, Page, Column, Container, Label, Theme

class HomePage(Page):
    def render(self):
        Label(self, text="Accueil", size="2xl", weight="bold")

app = App(title="Application", size=(1000, 700))

sidebar = Sidebar(app, title="Menu", items=[
    {"key": "home", "text": "Accueil", "icon": "home", "route": "/"},
], app=app)

right = Column(app, spacing=0)
Navbar(right, title="Accueil")
Container(right, padding=12, fill=True, expand=True)
Footer(right, text="© 2026 PyUI")

app.add_route("/", HomePage)
app.set_content(right.children[1])  # le Container
app.navigate("/")
app.run()
```