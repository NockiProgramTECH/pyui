"""Bouton radio PyUI (Niveau 1)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class RadioButton(Component):
    """Bouton radio (choix exclusif au sein d'un groupe).

    Le groupe est identifié par une chaîne partagée entre les radios.

    Exemple :
        RadioButton(parent, text="Option A", value="a", group="options", command=on_select)
        RadioButton(parent, text="Option B", value="b", group="options")
    """

    _tk_class = tk.Radiobutton
    _groups = {}

    def __init__(self, parent=None, text="", value=None, group=None, command=None):
        group = group or "default"
        self._var = self._groups.setdefault(group, tk.StringVar())
        self._text = text
        self._value = str(value) if value is not None else text
        self.command = command
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "text": self._text,
            "variable": self._var,
            "value": self._value,
            "command": self.command,
            "relief": tk.FLAT,
            "bd": 0,
            "highlightthickness": 0,
            "cursor": "hand2",
            "font": Theme.font("base"),
            "anchor": "w",
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
    def is_selected(self):
        return self._var.get() == self._value

    @is_selected.setter
    def is_selected(self, value):
        if value:
            self._var.set(self._value)