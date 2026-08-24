"""Cadre PyUI (Frame) (Niveau 1)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Frame(Component):
    """Cadre générique.

    Exemple :
        Frame(parent, padding=8)
    """

    _tk_class = tk.Frame
    bg_token = "surface"

    def __init__(self, parent=None, padding=0):
        self.padding = padding
        super().__init__(parent)

    def _apply_theme(self):
        self._apply_bg()