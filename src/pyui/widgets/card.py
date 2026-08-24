"""Carte PyUI (Niveau 2) : bloc visuel avec titre, optionnel sous-titre, fond surface.

Exemple :
    Card(parent, title="Chiffre d'affaires", subtitle="Année 2026")
"""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme
from pyui.widgets.label import Label


class Card(Component):
    """Conteneur stylisé. Les enfants créés avec parent=Card sont placés sous le titre."""

    _tk_class = tk.Frame
    bg_token = "surface"

    def __init__(self, parent=None, title=None, subtitle=None, padding=16):
        self.title = title
        self.subtitle = subtitle
        self.padding = padding
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "bg": Theme.get("surface"),
            "highlightthickness": 1,
            "highlightbackground": Theme.get("border"),
            "bd": 0,
            **super()._widget_kwargs(**kwargs),
        }

    def render(self):
        if self.title:
            self._title_label = Label(self, text=self.title, size="lg", weight="bold")
            self._title_label.pack(fill="x", anchor="w")
        if self.subtitle:
            self._subtitle_label = Label(self, text=self.subtitle, size="sm", color="muted")
            self._subtitle_label.pack(fill="x", anchor="w", pady=(2, 0))

    def set_title(self, title):
        """Met à jour le titre affiché."""
        self.title = title
        if getattr(self, "_title_label", None) is not None:
            self._title_label.text = title

    def set_subtitle(self, subtitle):
        """Met à jour le sous-titre affiché."""
        self.subtitle = subtitle
        if getattr(self, "_subtitle_label", None) is not None:
            self._subtitle_label.text = subtitle

    def _apply_theme(self):
        if self._tk is not None:
            self._tk.configure(
                bg=Theme.get("surface"),
                highlightbackground=Theme.get("border"),
            )