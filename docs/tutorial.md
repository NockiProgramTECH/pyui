# Tutoriel : première application de gestion

Ce tutoriel vous guide pas à pas pour créer une application de gestion de clients avec Sidebar, navigation, formulaire de saisie, tableau de données et thème sombre.

## 1. Structure

```python
from pyui import (
    App, Page, Sidebar, Navbar, Footer, Container, Column,
    Label, Card, Button, Input, Form, TextField, EmailField,
    DataTable, Theme, Toast,
)
```

## 2. Classe applicative

Créez une classe `AppGest` qui initialise l'application :

```python
class AppGest:
    def __init__(self):
        self.app = App(title="Gestion — PyUI", size=(1100, 700))
        self.clients = []
        self._setup_ui()
        self._setup_routes()
        self.app.navigate("/")
        self.app.run()

    def _setup_ui(self):
        sidebar = Sidebar(self.app, title="Gestion", items=[
            {"key": "dashboard", "text": "Dashboard", "icon": "home", "route": "/"},
            {"key": "clients", "text": "Clients", "icon": "users", "route": "/clients"},
            {"key": "ajout", "text": "Nouveau client", "icon": "plus", "route": "/ajout"},
        ], app=self.app)

        right = Column(self.app, spacing=0)
        self.navbar = Navbar(right, title="Dashboard", actions=[
            {"icon": "bell", "variant": "ghost"},
            {"text": "Thème", "icon": "settings", "variant": "ghost",
             "command": self._toggle_theme},
        ])
        self.content = Container(right, padding=12, fill=True, expand=True)
        self.app.set_content(self.content)
        Footer(right, text="© 2026 PyUI — Application de gestion")

    def _toggle_theme(self):
        if Theme.mode() == "light":
            Theme.dark()
            self.navbar.set_title("Mode sombre")
        else:
            Theme.light()
            self.navbar.set_title("Mode clair")
```

## 3. Pages

Définissez les pages comme des sous-classes de `Page` :

```python
class DashboardPage(Page):
    def __init__(self, parent, app_ref, **kwargs):
        self.app_ref = app_ref
        super().__init__(parent, **kwargs)

    def render(self):
        Label(self, text="Dashboard", size="2xl", weight="bold")
        total = len(self.app_ref.clients)
        Card(self, title="Clients", subtitle=f"{total} enregistrés")
        Card(self, title="Actions", subtitle="Utilisez le menu latéral")


class ClientsListPage(Page):
    def __init__(self, parent, app_ref, **kwargs):
        self.app_ref = app_ref
        super().__init__(parent, **kwargs)

    def render(self):
        Label(self, text="Liste des clients", size="2xl", weight="bold")
        Card(self, title="Clients", subtitle=f"{len(self.app_ref.clients)} enregistrements")
        DataTable(self, columns=[
            ("nom", "Nom"),
            ("email", "Email"),
            ("telephone", "Téléphone"),
        ], data=self.app_ref.clients, searchable=True, paginate=True, page_size=5,
            on_delete=lambda r: self._supprimer(r))


class AjoutClientPage(Page):
    def __init__(self, parent, app_ref, **kwargs):
        self.app_ref = app_ref
        super().__init__(parent, **kwargs)

    def render(self):
        Label(self, text="Nouveau client", size="2xl", weight="bold")
        Card(self, title="Informations")
        self.form = Form(self, fields=[
            TextField("nom", label="Nom", required=True, min_length=2),
            EmailField("email", label="Email", required=True),
            TextField("telephone", label="Téléphone", required=True),
        ], buttons=[
            {"text": "Enregistrer", "icon": "save", "variant": "primary", "type": "submit"},
            {"text": "Annuler", "variant": "ghost", "command": lambda: self.app.navigate("/")},
        ], on_submit=self._ajouter)

    def _ajouter(self, values):
        self.app_ref.clients.append(values)
        Toast.success(f"Client {values['nom']} ajouté")
        self.app.navigate("/clients")
```

## 4. Routes et lancement

```python
def _setup_routes(self):
    self.app.add_route("/", lambda: DashboardPage(self.content, app_ref=self))
    self.app.add_route("/clients", lambda: ClientsListPage(self.content, app_ref=self))
    self.app.add_route("/ajout", lambda: AjoutClientPage(self.content, app_ref=self))
```

## 5. Code complet

Le code complet de cette application se trouve dans `examples/06_gest_clients.py`.

## Concepts clés

- **`App`** : fenêtre racine, gère les routes, le thème et les événements
- **`Component`** : classe de base avec cycle de vie `create → render → update → destroy`
- **`Page`** : conteneur plein écran associé à une route
- **`Sidebar`** : menu latéral avec icônes, sous-menus et navigation intégrée
- **`Navbar`** : barre de titre avec actions (thème, notifications...)
- **`Form`** : générateur de formulaires avec validation automatique
- **`DataTable`** : tableau triable, paginé, avec recherche et export CSV
- **`Theme`** : design system avec `light()` / `dark()` et configuration des tokens
- **`Toast`** : notifications éphémères (`success`, `error`, `warning`, `info`)
- **`Dialog.confirm`** : boîte de dialogue de confirmation