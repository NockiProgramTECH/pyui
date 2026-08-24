"""Pied de page PyUI (Phase 4)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme
from pyui.widgets.label import Label


class Footer(Component):
    """Zone basse de l'application (copyright, version...)."""

    _tk_class = tk.Frame

    def __init__(self, parent=None, text=""):
        self.footer_text = text
        super().__init__(parent)
        self.pack(side="bottom", fill="x")

    def render(self):
        self._label = Label(self, text=self.footer_text, color="muted", size="sm")
        self._label.pack(pady=8)

    def _apply_theme(self):
        self._apply_bg()