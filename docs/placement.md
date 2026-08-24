# Placement des widgets (pack, grid, place)

Tout composant se positionne dans son parent grâce à **trois modèles de placement**,
sans aucun `**kwargs` : chaque paramètre est listé et validé.

```python
label.pack(side="top", fill="x", padx=8)
button.grid(row=0, column=1, sticky="nsew")
image.place(x=10, y=10, width=100)
```

## 1. `pack()` — empilement

Les widgets s'empilent le long d'un côté du parent.

```python
widget.pack(side="top", fill=None, expand=False, anchor=None,
            padx=0, pady=0, ipadx=0, ipady=0)
```

| Paramètre | Valeurs possibles | Défaut | Description |
|-----------|-------------------|--------|-------------|
| `side` | `"top"`, `"bottom"`, `"left"`, `"right"` | `"top"` | Côté du parent contre lequel empiler |
| `fill` | `None`, `"x"`, `"y"`, `"both"` | `None` | Étirer le widget : `"x"` (largeur), `"y"` (hauteur), `"both"` (les deux) |
| `expand` | `True`, `False` | `False` | Occuper l'espace libre restant du parent |
| `anchor` | `"n"`, `"s"`, `"e"`, `"w"`, `"ne"`, `"nw"`, `"se"`, `"sw"`, `"center"` | `None` | Position dans la zone allouée (si non étiré) |
| `padx` | entier ou tuple `(gauche, droite)` | `0` | Marge externe horizontale (px) |
| `pady` | entier ou tuple `(haut, bas)` | `0` | Marge externe verticale (px) |
| `ipadx` | entier ou tuple | `0` | Marge interne horizontale (px) |
| `ipady` | entier ou tuple | `0` | Marge interne verticale (px) |

**Exemples :**

```python
label.pack(fill="x", pady=(8, 0))          # pleine largeur, marge en haut
btn.pack(side="left", padx=4)              # bouton à gauche
sidebar.pack(side="left", fill="y")        # barre latérale pleine hauteur
```

## 2. `grid()` — grille en lignes/colonnes

Place le widget dans une cellule définie par sa ligne et sa colonne.

```python
widget.grid(row=None, column=None, rowspan=1, columnspan=1,
            sticky=None, padx=0, pady=0, ipadx=0, ipady=0)
```

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `row` | int (0, 1, 2...) | `None` | Ligne de la cellule |
| `column` | int (0, 1, 2...) | `None` | Colonne de la cellule |
| `rowspan` | int ≥ 1 | `1` | Nombre de lignes fusionnées |
| `columnspan` | int ≥ 1 | `1` | Nombre de colonnes fusionnées |
| `sticky` | combinaison de `"n"`, `"s"`, `"e"`, `"w"` | `None` | Étirement vers ces côtés (ex : `"nsew"` = plein cadre) |
| `padx` | entier ou tuple | `0` | Marge externe horizontale (px) |
| `pady` | entier ou tuple | `0` | Marge externe verticale (px) |
| `ipadx` | entier ou tuple | `0` | Marge interne horizontale (px) |
| `ipady` | entier ou tuple | `0` | Marge interne verticale (px) |

**Exemples :**

```python
titre.grid(row=0, column=0, columnspan=2, sticky="w")
zone.grid(row=1, column=0, sticky="nsew")
```

## 3. `place()` — position absolue

Place le widget à une position (en pixels ou en relatif) dans son parent.

```python
widget.place(x=None, y=None, relx=None, rely=None, anchor=None,
             width=None, height=None, relwidth=None, relheight=None)
```

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `x`, `y` | int | `None` | Position en pixels depuis le coin supérieur gauche |
| `relx`, `rely` | nombre 0.0 → 1.0 | `None` | Position relative à la taille du parent |
| `anchor` | `"nw"`, `"n"`, `"center"`, `"e"`, `"sw"`... | `None` | Point d'ancrage du widget sur la position |
| `width`, `height` | int | `None` | Taille en pixels |
| `relwidth`, `relheight` | nombre 0.0 → 1.0 | `None` | Taille relative au parent |

**Exemples :**

```python
logo.place(x=10, y=10, width=48, height=48)
overlay.place(relx=0.5, rely=0.5, anchor="center")
```

## 4. Le modèle de placement (`Pack`, `GridPlacement`, `Place`)

Chaque méthode crée un **modèle** stocké dans `widget.placement`.
Le modèle est conservé : `show()` et `hide()` restaurent exactement le
même placement (marges, étirement, côté...).

On peut aussi construire un placement réutilisable et l'appliquer :

```python
from pyui import Pack, Place, GridPlacement

gauche = Pack(side="left", fill="y", padx=8)
menu.layout(gauche)
panel.layout(gauche)

centré = Place(relx=0.5, rely=0.5, anchor="center")
dialog.layout(centré)
```

| Classe | Modèle | Paramètres identiques à |
|--------|--------|-------------------------|
| `Pack` | empilement | `pack()` |
| `GridPlacement` | grille | `grid()` |
| `Place` | absolu | `place()` |

Méthodes utiles :
- `widget.layout(placement)` : applique un modèle (remplace l'ancien)
- `widget.placement` : le modèle actuel (`Pack`, `GridPlacement` ou `Place`)
- `placement.to_dict()` : les paramètres sous forme de dict
- `placement.remove(widget)` : retire le widget de son conteneur

## 5. Erreurs claires pour les débutants

Les valeurs invalides lèvent une `ValueError` avec un message explicite :

```python
label.pack(side="droite")      # ValueError: side invalide : 'droite'...
label.pack(fill="xet")         # ValueError: fill invalide...
label.pack(padx="10")          # ValueError: padx doit être un entier...
```

## 6. Règles d'or

1. **Un seul gestionnaire par parent** : ne mélangez pas `pack()` et `grid()`
   pour les enfants d'un même conteneur.
2. **`pack`** pour les interfaces en flux (colonnes, barres) ;
   **`grid`** pour les grilles de formulaire ; **`place`** pour les overlays
   et positions précises.
3. Pour les layouts tout faits, préférez `Row`, `Column`, `Grid` et `Stack`
   (voir [layouts](layouts.md)) qui gèrent le placement automatiquement.
