"""Colonne PyUI (Niveau 3) : enfants placés de haut en bas."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Column(Component):
    """Place automatiquement ses enfants verticalement (étirés par défaut).

    Exemple :
        col = Column(parent, spacing=8)
        Label(col, text="Nom")
        Input(col, placeholder="Votre nom")
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, children=None, spacing=8, align="stretch"):
        self.spacing = spacing
        self.align = align
        super().__init__(parent)
        if children:
            for child in children:
                self.add(child)

    def _add_child(self, child):
        super()._add_child(child)
        fill = "x" if self.align == "stretch" else None
        pad = self.spacing // 2
        child.pack(fill=fill, padx=pad, pady=pad)

    def add(self, item, **kwargs):
        """Ajoute un composant (ou une classe de composant) à la colonne.

        Renvoie la colonne pour permettre l'enchaînement.
        """
        if isinstance(item, type):
            item = item(self, **kwargs)
        elif item.parent is not self:
            raise ValueError("Ce composant est déjà rattaché à un autre parent")
        return self

    def _apply_theme(self):
        self._apply_bg()