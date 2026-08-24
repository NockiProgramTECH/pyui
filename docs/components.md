# Composants (widgets)

## Classe de base : `Component`

Tous les composants héritent de `Component` et respectent le cycle de vie :

```
create → render → update → destroy
```

### API commune

| Méthode | Description |
|---------|-------------|
| `show()` | Affiche le composant |
| `hide()` | Masque le composant |
| `destroy()` | Détruit le composant et ses enfants |
| `configure(**kwargs)` | Met à jour les propriétés |
| `update(**kwargs)` | Alias de configure |
| `pack(...)` | Positionne en pack |
| `grid(...)` | Positionne en grille |
| `place(...)` | Positionne en absolu |
| `bind(sequence, callback)` | Lie un événement Tkinter |
| `focus()` | Donne le focus |

### Attributs

| Attribut | Description |
|----------|-------------|
| `parent` | Composant parent |
| `children` | Liste des enfants |
| `tk` | Widget Tkinter sous-jacent |

---

## `Button`

Bouton cliquable avec variantes et effet hover.

```python
Button(parent, text="Enregistrer", command=save, variant="primary", icon="save")
```

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `text` | str | "" | Texte du bouton |
| `command` | callable | None | Fonction appelée au clic |
| `variant` | str | "primary" | "primary", "secondary", "success", "danger", "warning", "ghost", "outline" |
| `icon` | str | None | Nom d'icône (voir IconManager) |
| `disabled` | bool | False | Désactive le bouton |
| `width` | int | None | Largeur en caractères |

**Méthodes** : `enable()`, `disable()`, `text` (propriété get/set)

---

## `Label`

Texte statique ou dynamique.

```python
Label(parent, text="Bonjour", size="xl", weight="bold", color="text")
```

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `text` | str | "" | Texte |
| `size` | str | "base" | "xs", "sm", "base", "lg", "xl", "2xl", "3xl" |
| `weight` | str | "normal" | "normal", "bold" |
| `color` | str | "text" | Jeton de couleur (Theme.get) |
| `anchor` | str | "w" | Position : "w", "center", "e" |

---

## `Input`

Champ de saisie texte avec placeholder.

```python
Input(parent, value="", placeholder="Nom", width=30)
```

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `value` | str | "" | Valeur initiale |
| `placeholder` | str | None | Texte indicatif (grisé) |
| `width` | int | 30 | Largeur en caractères |
| `show` | str | None | Caractère de masquage (ex : `"•"` pour un mot de passe) |

**Méthodes** : `get()`, `set(value)`

---

## `Text`

Zone de texte multiligne.

```python
Text(parent, value="Contenu", height=8, width=40)
```

**Méthodes** : `get()`, `set(value)`

---

## `CheckBox`

Case à cocher.

```python
CheckBox(parent, text="Activer", checked=True, command=on_toggle)
```

**Propriétés** : `is_checked` (get/set)

---

## `RadioButton`

Bouton radio (choix exclusif par groupe).

```python
RadioButton(parent, text="A", value="a", group="options", command=on_select)
RadioButton(parent, text="B", value="b", group="options")
```

**Propriétés** : `is_selected` (get/set)

---

## `Select`

Liste déroulante.

```python
Select(parent, options=["A", "B"], value="A", command=on_select)
```

**Méthodes** : `get()`, `set(value)`

---

## `ListBox`

Liste de sélection.

```python
ListBox(parent, items=["A", "B"], selectmode="single", on_select=callback)
```

**Méthodes** : `get_selected()`, `get_selected_index()`

---

## `ProgressBar`

Barre de progression.

```python
ProgressBar(parent, value=50, maximum=100, mode="determinate")
```

**Méthodes** : `set(value)`, `advance(delta=1)`

---

## `Separator`

Ligne de séparation.

```python
Separator(parent, orientation="horizontal")
```

---

## `Frame`

Cadre générique.

```python
Frame(parent, padding=0)
```

---

## `Card`

Carte avec titre et sous-titre.

```python
Card(parent, title="Chiffre d'affaires", subtitle="2 450 000 FCFA")
```

**Méthodes** : `set_title(title)`, `set_subtitle(subtitle)`

---

## `StatCard`

Carte statistique (Dashboard).

```python
StatCard(parent, title="Clients", value="1 245", icon="users", delta="+12%")
```

---

## `Badge`

Étiquette colorée.

```python
Badge(parent, text="Actif", variant="success")
```

Variantes : `default`, `primary`, `success`, `danger`, `warning`, `outline`

## `Alert`

Message coloré avec fermeture optionnelle.

```python
Alert(parent, message="Client enregistré", variant="success", dismissible=True)
```

Variantes : `info`, `success`, `warning`, `danger`

## `Tooltip`

Infobulle au survol d'un composant.

```python
Tooltip(button, text="Enregistrer les modifications", delay=400)
```

## `Spinner`

Animation de chargement (Canvas).

```python
spinner = Spinner(parent, size=28, color="primary")
spinner.start()  # / spinner.stop()
```

## `Loading`

Surcouche de chargement avec spinner + message.

```python
loading = Loading(app, message="Chargement...")
loading.open()
# ... opération ...
loading.close()
```

## `Tabs`

Onglets avec zone de contenu.

```python
Tabs(parent, tabs=[
    {"text": "Clients", "content": ClientsTab},   # sous-classe de Component
    {"text": "Ventes",  "content": lambda p: Label(p, text="Ventes")},
])
tabs.select(0)  # / tabs.index
```

## `Accordion`

Sections repliables.

```python
Accordion(parent, sections=[
    {"title": "Général", "content": lambda p: Label(p, text="Contenu")},
])
acc.toggle(0)
```

## `Modal`

Fenêtre modale avec titre et contenu.

```python
modal = Modal(app, title="Confirmation", content=ConfirmPanel)
modal.open()
modal.close()
```