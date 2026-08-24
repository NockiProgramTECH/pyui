"""Case à cocher PyUI (Niveau 1)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class CheckBox(Component):
    """Case à cocher avec état booléen.

    Exemple :
        CheckBox(parent, text="Activer", checked=True, command=on_toggle)
    """

    _tk_class = tk.Checkbutton

    def __init__(self, parent=None, text="", checked=False, command=None):
        self._var = tk.BooleanVar(value=bool(checked))
        self.command = command
        self._text = text
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "text": self._text,
            "variable": self._var,
            "command": self.command,
            "relief": tk.FLAT,
            "bd": 0,
            "highlightthickness": 0,
            "cursor": "hand2",
            "font": Theme.font("base"),
            "anchor": "w",
            "justify": "left",
            **super()._widget_kwargs(**kwargs),
        }

    def _apply_theme(self):
        if self._tk is None:
            return
        parent_bg = Theme.get(getattr(self.parent, "bg_token", "background"))
        surface = Theme.get("surface")
        fg = Theme.get("text")
        self._tk.configure(
            bg=parent_bg, fg=fg,
            activebackground=parent_bg, activeforeground=fg,
            selectcolor=surface,
        )

    @property
    def is_checked(self):
        return self._var.get()

    @is_checked.setter
    def is_checked(self, value):
        self._var.set(bool(value))