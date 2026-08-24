# Référence API complète

## `App`

```python
App(title="PyUI", size=(1000, 700), min_size=(800, 600), theme="light")
```

| Méthode | Description |
|---------|-------------|
| `run()` | Lance la boucle d'événements (bloquant) |
| `close()` | Ferme l'application |
| `add_route(path, page_cls, title=None, name=None)` | Enregistre une route |
| `navigate(path, record=True)` | Affiche une page, émet `navigate` |
| `back()` | Revient à la page précédente (historique) |
| `forward()` | Avance après un retour (historique) |
| `set_content(container)` | Définit le conteneur des pages |
| `before_navigate(callback)` | Hook appelé avant chaque navigation |
| `after_navigate(callback)` | Hook appelé après chaque navigation |

Propriétés : `current_path`, `can_back`, `can_forward`, `page`, `routes()`.

Attributs : `title`, `theme`, `events` (EventBus), `state` (State), `router` (Router), `tk`.

## `Router` et `Route`

```python
router = Router()
router.add("/", HomePage, title="Accueil")
router.push("/clients")
router.back() / forward() / reset()
router.current_path / current_route / can_back / can_forward
```

## `Component`

Cycle de vie `create → render → update → destroy`.

### Méthodes communes

| Méthode | Description |
|---------|-------------|
| `show()` | Affiche (restaure le placement) |
| `hide()` | Masque (conserve le placement) |
| `destroy()` | Détruit le composant et ses enfants |
| `configure(**tk_options)` | Options Tkinter natives (niveau avancé) |
| `bind(sequence, callback)` | Lie un événement Tkinter |
| `focus()` | Donne le focus |
| `layout(placement)` | Applique un modèle `Pack` / `GridPlacement` / `Place` |

### Placement — paramètres explicites (aucun `**kwargs`)

```python
pack(side="top", fill=None, expand=False, anchor=None, padx=0, pady=0, ipadx=0, ipady=0)
grid(row=None, column=None, rowspan=1, columnspan=1, sticky=None, padx=0, pady=0, ipadx=0, ipady=0)
place(x=None, y=None, relx=None, rely=None, anchor=None, width=None, height=None, relwidth=None, relheight=None)
```

> Toutes les valeurs possibles : voir [placement.md](placement.md).

Attributs : `parent`, `children`, `tk`, `placement`.

## Modèles de placement

```python
from pyui import Pack, GridPlacement, Place

Pack(side="left", fill="y", padx=8)
GridPlacement(row=0, column=1, sticky="nsew")
Place(relx=0.5, rely=0.5, anchor="center")
```

- `placement.to_dict()` : paramètres en dict
- `placement.remove(widget)` : retire le widget

## `Page`

Sous-classe de `Component`. `Page(parent, app=None, route=None, title=None, padding=16)`.
Attributs : `app`, `route`, `page_title`.

## Widgets

| Classe | Construction |
|--------|-------------|
| `Button` | `Button(parent, text="", command=None, variant="primary", icon=None, disabled=False)` |
| `Label` | `Label(parent, text="", size="base", weight="normal", color="text")` |
| `Input` | `Input(parent, value="", placeholder=None, width=30)` |
| `Text` | `Text(parent, value="", height=8, width=40)` |
| `CheckBox` | `CheckBox(parent, text="", checked=False, command=None)` |
| `RadioButton` | `RadioButton(parent, text="", value=None, group=None, command=None)` |
| `Select` | `Select(parent, options=[], value=None, state="readonly", command=None)` |
| `ListBox` | `ListBox(parent, items=[], selectmode="single", on_select=None)` |
| `ProgressBar` | `ProgressBar(parent, value=0, maximum=100, mode="determinate")` |
| `Separator` | `Separator(parent, orientation="horizontal")` |
| `Frame` | `Frame(parent, padding=0)` |
| `Card` | `Card(parent, title=None, subtitle=None, padding=16)` |
| `StatCard` | `StatCard(parent, title="", value="", icon=None, delta=None)` |
| `Badge` | `Badge(parent, text="", variant="default", size="sm")` |
| `Alert` | `Alert(parent, message="", variant="info", dismissible=False, icon=None)` |
| `Tooltip` | `Tooltip(widget, text="", delay=400)` |
| `Spinner` | `Spinner(parent, size=24, color="primary", speed=60)` — `start()`, `stop()` |
| `Loading` | `Loading(parent, message="Chargement...", spinner_size=32)` — `open()`, `close()` |
| `Tabs` | `Tabs(parent, tabs=[{"text", "content"}])` — `select(index)`, `index` |
| `Accordion` | `Accordion(parent, sections=[{"title", "content"}])` — `toggle(index)` |
| `Modal` | `Modal(parent, title="", content=None, on_close=None)` — `open()`, `close()`, `wait()` |

## Layouts

| Classe | Construction |
|--------|-------------|
| `Container` | `Container(parent, padding=0, fill=True, expand=True)` |
| `Row` | `Row(parent, children=None, spacing=8, align="center")` |
| `Column` | `Column(parent, children=None, spacing=8, align="stretch")` |
| `Stack` | `Stack(parent, children=None, spacing=8)` |
| `Grid` | `Grid(parent, columns=2, spacing=8)` |
| `Sidebar` | `Sidebar(parent, items=[], title=None, logo=None, width=240, position="left", active=None, app=None)` |
| `Navbar` | `Navbar(parent, title="", actions=[], height=56)` |
| `Footer` | `Footer(parent, text="")` |

## Dashboard

| Classe | Construction |
|--------|-------------|
| `Dashboard` | `Dashboard(parent, stats=[], chart={}, activity=[], timeline=[], actions=[], columns=4)` |
| `Chart` | `Chart(parent, kind="line", data=[], title=None, height=240)` — `set_data()` |
| `Activity` | `Activity(parent, items=[{"icon","text","time"}])` |
| `Timeline` | `Timeline(parent, items=[{"title","time","text","color"}])` |
| `QuickAction` | `QuickAction(parent, text="", icon=None, command=None)` |
| `Metric` | `Metric(parent, label="", value="")` |

## Formulaires

```python
Form(parent, fields=[...], on_submit=None, buttons=None, spacing=10)
```

Champs : `TextField`, `PasswordField`, `EmailField`, `NumberField`,
`SelectField`, `CheckboxField`, `DateField`, `FileField`.

Options communes : `name`, `label`, `required`, `min_length`, `max_length`,
`pattern`, `validator`, `help_text`, `initial`.

`NumberField` : `min`, `max`. `SelectField` : `options`.

Méthodes Form : `values()`, `set_values(d)`, `validate()`, `submit()`, `clear()`, `get_field(name)`.

## Tableau

```python
DataTable(parent, columns=[...], data=[...], searchable=True, paginate=True,
          page_size=10, selectable=True, multi_select=False, sortable=True,
          on_select=None, on_double_click=None, on_edit=None, on_delete=None,
          row_actions=None, exportable=False)
```

Méthodes : `set_data`, `add_row`, `update_row`, `remove_row`, `clear`,
`set_filter`, `selected_rows`, `previous_page`, `next_page`, `export`.

## Thème

```python
Theme.light() / Theme.dark() / Theme.set_mode(mode) / Theme.mode()
Theme.get(token, default=None) / Theme.configure(**tokens)
Theme.font(size="base", weight="normal")
Theme.subscribe(callback)
```

## Icônes

```python
IconManager.glyph(name) → str
GLYPHS → dict
```

## Dialogues et notifications

```python
Dialog.confirm(message, on_confirm=None, on_cancel=None, title="Confirmation")
Dialog.error(message) / Dialog.warning(message) / Dialog.success(message) / Dialog.info(message)
Toast.success(message) / Toast.error(message) / Toast.warning(message) / Toast.info(message)
```

## État et événements

```python
State(initial={})
state.get(key, default=None) / state.set(key, value) / state.update(**data)
state.has(key) / state.snapshot() / state.reset() / state.replace(data)
state.subscribe(key, callback) / state.subscribe(callback) / state.unsubscribe(key, cb)
state.bind(component, key, target=None)     # → fonction de désabonnement

Component.bind_state(state, key, target=None)  # auto-désabonnement à la destruction

EventBus()         # on, off, emit
```