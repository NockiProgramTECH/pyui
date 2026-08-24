"""Champ de saisie PyUI (Entry) avec placeholder (Niveau 1)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Input(Component):
    """Champ de saisie texte avec placeholder.

    Exemple :
        Input(parent, value="", placeholder="Entrez votre nom", width=30)
    """

    _tk_class = tk.Entry

    def __init__(self, parent=None, value="", placeholder=None, width=30,
                 show=None):
        self._value = value
        self.placeholder = placeholder
        self.width = width
        self.show = show
        self._filled = bool(value)
        self._placeholder_shown = False
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        options = {
            "width": self.width,
            "relief": tk.FLAT,
            "bd": 0,
            "highlightthickness": 1,
            "insertwidth": 2,
        }
        if self.show is not None:
            options["show"] = self.show
        return {**options, **super()._widget_kwargs(**kwargs)}

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
        if self._value and not self._tk.get():
            self._tk.insert(0, self._value)
        self._setup_placeholder()

    def _setup_placeholder(self):
        if not self.placeholder:
            return
        self.bind("<FocusIn>", lambda e: self._on_focus_in(e), add="+")
        self.bind("<FocusOut>", lambda e: self._on_focus_out(e), add="+")
        self._on_focus_out(None)

    def _on_focus_in(self, event):
        if self._placeholder_shown:
            self._tk.delete(0, "end")
            self._tk.configure(fg=Theme.get("text"))
            self._placeholder_shown = False

    def _on_focus_out(self, event):
        if not self._tk.get():
            self._tk.insert(0, self.placeholder or "")
            self._tk.configure(fg=Theme.get("muted"))
            self._placeholder_shown = True
        else:
            self._placeholder_shown = False

    def get(self):
        if self._tk is None:
            return self._value
        val = self._tk.get()
        if self._placeholder_shown and val == self.placeholder:
            return ""
        return val

    def set(self, value):
        self._value = value
        if self._tk is not None:
            self._tk.delete(0, "end")
            if value:
                self._tk.insert(0, value)
                self._tk.configure(fg=Theme.get("text"))
                self._placeholder_shown = False
            else:
                self._on_focus_out(None)