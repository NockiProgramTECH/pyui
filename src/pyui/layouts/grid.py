"""Grille PyUI (Niveau 3) : placement en lignes et colonnes uniformes."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Grid(Component):
    """Grille régulière : les enfants sont placés automatiquement ligne par ligne.

    Exemple :
        grid = Grid(parent, columns=3, spacing=8)
        Card(grid, title="A")
        Card(grid, title="B")
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, columns=2, spacing=8):
        self.columns = max(1, columns)
        self.spacing = spacing
        self._index = 0
        super().__init__(parent)

    def _add_child(self, child):
        super()._add_child(child)
        row, col = divmod(self._index, self.columns)
        self._index += 1
        for i in range(self.columns):
            self._tk.columnconfigure(i, weight=1, uniform="pyui_grid")
        pad = self.spacing // 2
        child.grid(row=row, column=col, sticky="nsew", padx=pad, pady=pad)

    def add(self, item, **kwargs):
        """Ajoute un composant (ou une classe de composant) à la grille.

        Renvoie la grille pour permettre l'enchaînement.
        """
        if isinstance(item, type):
            item = item(self, **kwargs)
        elif item.parent is not self:
            raise ValueError("Ce composant est déjà rattaché à un autre parent")
        return self

    def _apply_theme(self):
        self._apply_bg()