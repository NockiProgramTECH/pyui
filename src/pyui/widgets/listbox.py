"""Liste de sélection PyUI (ListBox) (Niveau 1)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class ListBox(Component):
    """Liste déroulable avec sélection simple ou multiple.

    Exemple :
        ListBox(parent, items=["A", "B", "C"], selectmode="single", on_select=callback)
    """

    _tk_class = tk.Listbox

    def __init__(self, parent=None, items=None, selectmode="single",
                 height=8, on_select=None):
        self._items = list(items or [])
        self._var = tk.StringVar(value=list(self._items))
        self.selectmode = selectmode
        self.height = height
        self.on_select = on_select
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "listvariable": self._var,
            "selectmode": self.selectmode,
            "relief": tk.FLAT,
            "bd": 0,
            "highlightthickness": 1,
            "height": self.height,
            "exportselection": False,
            "font": Theme.font("base"),
            **super()._widget_kwargs(**kwargs),
        }

    def _apply_theme(self):
        if self._tk is None:
            return
        self._tk.configure(
            bg=Theme.get("surface"),
            fg=Theme.get("text"),
            selectbackground=Theme.get("primary"),
            selectforeground=Theme.get("on_primary"),
            highlightbackground=Theme.get("border"),
            highlightcolor=Theme.get("primary"),
        )

    def render(self):
        if self.on_select is not None:
            self._tk.bind("<<ListboxSelect>>", lambda e: self.on_select(self))

    def get_selected(self):
        if self._tk is None:
            return []
        indices = self._tk.curselection()
        return [self._items[i] for i in indices]

    def get_selected_index(self):
        if self._tk is None:
            return None
        indices = self._tk.curselection()
        return indices[0] if indices else None