"""Définition des colonnes d'un DataTable."""


class Column:
    """Colonne : clé, titre, largeur, alignement, triable."""

    def __init__(self, key, title=None, width=None, align="left", sortable=True):
        self.key = key
        self.title = title or key
        self.width = width
        self.align = align
        self.sortable = sortable
