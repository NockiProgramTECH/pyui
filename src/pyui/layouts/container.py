"""Conteneur de base PyUI (Niveau 3)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Container(Component):
    """Zone de contenu avec padding, qui s'étire par défaut.

    Exemple :
        Container(parent, padding=16)
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, padding=0, fill=True, expand=True):
        self.padding = padding
        super().__init__(parent)
        if fill or expand:
            self.pack(fill="both" if fill else None, expand=expand,
                      padx=padding, pady=padding)

    def _apply_theme(self):
        self._apply_bg()