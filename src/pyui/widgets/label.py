"""Libellé PyUI (Niveau 1)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Label(Component):
    """Texte statique ou dynamique avec taille, poids et couleur.

    Exemple :
        Label(parent, text="Bonjour", size="xl", weight="bold", color="text")
    """

    _tk_class = tk.Label

    def __init__(self, parent=None, text="", size="base", weight="normal",
                 color="text", anchor="w"):
        self._text = text
        self.size = size
        self.weight = weight
        self.color = color
        self.anchor = anchor
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "text": self._text,
            "font": Theme.font(self.size, self.weight),
            "anchor": self.anchor,
            "justify": "left",
            **super()._widget_kwargs(**kwargs),
        }

    def _apply_theme(self):
        if self._tk is None:
            return
        parent_bg = getattr(self.parent, "bg_token", "background")
        self._tk.configure(
            fg=Theme.get(self.color, Theme.get("text")),
            bg=Theme.get(parent_bg),
        )

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        if self._tk is not None:
            self._tk.configure(text=value)