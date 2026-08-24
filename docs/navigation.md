# Navigation

## Routes

```python
app.add_route("/", DashboardPage, title="Dashboard")
app.add_route("/clients", ClientsPage, title="Clients")
app.navigate("/clients")
```

Options d'une route : `title` (titre affichable), `name` (identifiant).

## `Page`

Conteneur plein écran associé à une route.

```python
class DashboardPage(Page):
    def on_show(self):
        # appelé quand la page devient active
        pass

    def on_hide(self):
        # appelé quand la page quitte l'écran (avant destruction)
        pass

    def render(self):
        Label(self, text="Dashboard", size="2xl", weight="bold")
```

Attributs disponibles : `app`, `route`, `page_title`, `padding`.

## Historique de navigation

```python
app.navigate("/clients")
app.navigate("/products")

app.back()       # → revient à "/clients"
app.forward()    # → revient à "/products"

app.current_path  # chemin actuel
app.can_back      # bool
app.can_forward   # bool
```

## Hooks de navigation

```python
app.before_navigate(lambda path: print(f"Avant → {path}"))
app.after_navigate(lambda path, page: print(f"Après → {path}"))
```

## `Router`

Le `Router` est accessible via `app.router` :

```python
app.router.add("/dashboard", DashboardPage, title="Dashboard")
app.router.routes          # dict {chemin: Route}
app.router.current_path    # chemin actuel
app.router.current_route   # objet Route actuel (avec .title)
app.router.back() / forward() / push(path) / reset()
```

Utilisation autonome :

```python
router = Router()
router.add("/", HomePage)
router.push("/clients")
router.back()
```

## Navigation intégrée Sidebar

La `Sidebar` navigue automatiquement au clic sur un item avec `route` :

```python
sidebar = Sidebar(parent, items=[
    {"key": "home", "text": "Accueil", "route": "/"},
], app=app)
```

## Événement `navigate`

`App.navigate()` émet un événement `"navigate"` sur le bus d'événements :

```python
app.events.on("navigate", lambda event: print(f"Navigation vers {event.data['path']}"))
```

## `App.set_content()`

Permet d'injecter un conteneur personnalisé pour les pages (ex: colonne avec Navbar + Footer) :

```python
content = Container(right, padding=12, fill=True, expand=True)
app.set_content(content)
```