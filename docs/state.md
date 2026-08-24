# État réactif (State)

## `State`

État global observable avec abonnement par clé ou global.

```python
from pyui import State

state = State({"user": None, "theme": "light", "count": 0})

# Lecture
state.get("user")

# Écriture (notifie les abonnés)
state.set("theme", "dark")

# Multi-écriture
state.update(user="Awa", theme="dark")

# État complet
state.snapshot()          # → dict
state.has("user")         # → bool
state.reset()             # → retour à l'état initial
state.replace({"a": 1})   # → remplace tout
```

## Abonnement

```python
# Sur une clé précise
state.subscribe("theme", lambda key, value, old: print(value))

# Sur toutes les clés
state.subscribe(lambda key, value, old: print(f"{key} → {value}"))

# Désabonnement
unsub = state.subscribe("count", callback)
unsub()
```

Les callbacks reçoivent `(key, value, old_value)`. Une valeur inchangée ne déclenche pas de notification.

## Liaison aux composants

### `State.bind(component, key, target)`

```python
state.bind(label, "count", "text")                      # attribut / propriété
state.bind(button, "enabled", lambda b, v: b.enable() if v else b.disable())  # callable
```

`target` peut être :
- `None` : utilise le nom de la clé comme attribut
- `str` : nom de propriété (avec setter) du composant
- `callable(component, value)` : mise à jour personnalisée

### `Component.bind_state(state, key, target)`

Même chose, avec désabonnement automatique à la destruction du composant :

```python
count_label = Label(parent, text="0")
count_label.bind_state(state, "count", "text")
```

### Exemple complet

```python
state = State({"count": 0, "theme": "light"})

label = Label(parent, text="0")
label.bind_state(state, "count", "text")

Button(parent, text="+", command=lambda: state.set("count", state.get("count") + 1))
Button(parent, text="−", command=lambda: state.set("count", state.get("count") - 1))

# Thème piloté par l'état
state.subscribe("theme", lambda k, v, o: Theme.dark() if v == "dark" else Theme.light())
```

## Utilisation dans l'App

```python
app = App()
app.state.set("theme", "dark")
app.state.get("user")
```

Démo : `python examples/08_state.py`