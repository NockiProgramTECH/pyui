"""Ligne PyUI (Niveau 3) : enfants placés de gauche à droite."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Row(Component):
    """Place automatiquement ses enfants horizontalement.

    Exemple :
        row = Row(parent, spacing=8)
        Button(row, text="A")
        Button(row, text="B")
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, children=None, spacing=8, align="center"):
        self.spacing = spacing
        self.align = align
        super().__init__(parent)
        if children:
            for child in children:
                self.add(child)

    def _add_child(self, child):
        super()._add_child(child)
        pad = self.spacing // 2
        child.pack(side="left", padx=pad, pady=pad)

    def add(self, item, **kwargs):
        """Ajoute un composant (ou une classe de composant) à la ligne.

        Renvoie la ligne pour permettre l'enchaînement.
        """
        if isinstance(item, type):
            item = item(self, **kwargs)
        elif item.parent is not self:
            raise ValueError("Ce composant est déjà rattaché à un autre parent")
        return self

    def _apply_theme(self):
        self._apply_bg()