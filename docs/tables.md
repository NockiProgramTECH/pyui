# Table de données

## `DataTable`

Tableau complet basé sur `ttk.Treeview` avec tri, recherche, pagination, sélection, menu contextuel et export CSV.

```python
DataTable(
    parent,
    columns=[
        ("name", "Nom"),
        ("email", "Email"),
        ("phone", "Téléphone"),
    ],
    data=users,
    searchable=True,
    paginate=True,
    page_size=10,
    exportable=True,
    on_select=callback,
    on_double_click=callback,
    on_edit=edit_callback,
    on_delete=delete_callback,
    multi_select=False,
)
```

### Paramètres

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `columns` | list | (obligatoire) | Tuples `(key, titre)` ou `Column(key, title, width=100)` |
| `data` | list | [] | Liste de dicts `{key: valeur}` |
| `searchable` | bool | True | Barre de recherche |
| `paginate` | bool | True | Pagination avec contrôles |
| `page_size` | int | 10 | Lignes par page |
| `selectable` | bool | True | Sélection par clic |
| `multi_select` | bool | False | Sélection multiple |
| `sortable` | bool | True | Tri par clic sur en-tête |
| `height` | int | None | Hauteur du tableau (lignes) |
| `on_select` | callable | None | Appelé avec la liste des lignes sélectionnées |
| `on_double_click` | callable | None | Appelé avec la ligne double-cliquée |
| `on_edit` | callable | None | Menu contextuel "Modifier" |
| `on_delete` | callable | None | Menu contextuel "Supprimer" |
| `row_actions` | callable | None | `lambda row: [("Label", command), ...]` |
| `exportable` | bool | False | Bouton "Exporter CSV" |
| `empty_text` | str | "Aucune donnée" | Texte si vide |

### Méthodes

| Méthode | Description |
|---------|-------------|
| `set_data(data)` | Remplace les données |
| `add_row(row)` | Ajoute une ligne |
| `update_row(predicate, row)` | Met à jour la ligne correspondant à `predicate` |
| `remove_row(predicate)` | Supprime les lignes correspondant à `predicate` |
| `clear()` | Vide le tableau |
| `set_filter(predicate)` | Filtre personnalisé `lambda row: bool` |
| `selected_rows()` | Renvoie les lignes sélectionnées |
| `previous_page()` | Page précédente |
| `next_page()` | Page suivante |
| `export(filename)` | Exporte en CSV (séparateur ;, UTF-8 BOM) |

### Colonnes

```python
from pyui import TableColumn

columns = [
    TableColumn("name", "Nom", width=200, align="left", sortable=True),
    TableColumn("age", "Âge", width=80, align="center", sortable=True),
]
```