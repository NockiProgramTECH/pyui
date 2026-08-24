"""Zone de texte multiligne PyUI (Text)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Text(Component):
    """Éditeur de texte multiligne.

    Exemple :
        Text(parent, value="Contenu initial", height=10, width=50)
    """

    _tk_class = tk.Text

    def __init__(self, parent=None, value="", height=8, width=40):
        self._value = value
        self.height = height
        self.width = width
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "height": self.height,
            "width": self.width,
            "relief": tk.FLAT,
            "bd": 0,
            "highlightthickness": 1,
            "insertwidth": 2,
            "font": Theme.font("base"),
            "wrap": "word",
            **super()._widget_kwargs(**kwargs),
        }

    def _apply_theme(self):
        if self._tk is None:
            return
        fg = Theme.get("text")
        bg = Theme.get("surface")
        self._tk.configure(
            bg=bg, fg=fg, insertbackground=fg,
            highlightbackground=Theme.get("border"),
            highlightcolor=Theme.get("primary"),
            selectbackground=Theme.get("primary"),
            selectforeground=Theme.get("on_primary"),
        )
        if self._value and not self._tk.get("1.0", "end-1c"):
            self._tk.insert("1.0", self._value)

    def get(self):
        if self._tk is not None:
            return self._tk.get("1.0", "end-1c")
        return self._value

    def set(self, value):
        self._value = value
        if self._tk is not None:
            self._tk.delete("1.0", "end")
            self._tk.insert("1.0", value)