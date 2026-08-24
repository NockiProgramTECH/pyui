"""Badge PyUI (Niveau 2) : étiquette colorée."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Badge(Component):
    """Étiquette compacte avec couleur de variante.

    Exemple :
        Badge(parent, text="Actif", variant="success")
    """

    _tk_class = tk.Label

    _VARIANTS = {
        "default": {"bg": "secondary", "fg": "on_secondary"},
        "primary": {"bg": "primary",   "fg": "on_primary"},
        "success": {"bg": "success",   "fg": "on_success"},
        "danger":  {"bg": "danger",    "fg": "on_danger"},
        "warning": {"bg": "warning",   "fg": "on_warning"},
        "outline": {"bg": "surface",   "fg": "text"},
    }

    def __init__(self, parent=None, text="", variant="default", size="sm"):
        self._text = text
        self.variant = variant
        self.size = size
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "text": self._text,
            "font": Theme.font(self.size, "bold"),
            "padx": 8,
            "pady": 2,
            "bd": 0,
            **super()._widget_kwargs(**kwargs),
        }

    def _apply_theme(self):
        if self._tk is None:
            return
        v = self._VARIANTS.get(self.variant, self._VARIANTS["default"])
        self._tk.configure(bg=Theme.get(v["bg"]), fg=Theme.get(v["fg"]))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        if self._tk is not None:
            self._tk.configure(text=value)