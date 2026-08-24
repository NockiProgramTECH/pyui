"""Empilement vertical PyUI (Niveau 3)."""

from pyui.layouts.column import Column


class Stack(Column):
    """Colonne d'enfants empilés avec espacement (alias de Column).

    Exemple :
        Stack(parent, spacing=8)
    """