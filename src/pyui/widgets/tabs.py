"""Onglets PyUI (Niveau 2).

Exemple :
    tabs = Tabs(parent, tabs=[
        {"text": "Clients", "content": ClientsTab},        # sous-classe de Component
        {"text": "Ventes",  "content": lambda p: Label(p, text="Ventes")},
    ])
    tabs.select(0)
"""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Tabs(Component):
    """Navigation par onglets avec zone de contenu."""

    _tk_class = tk.Frame

    def __init__(self, parent=None, tabs=None):
        self.tabs_specs = list(tabs or [])
        self._index = 0
        self._tab_buttons = {}
        self._body = None
        self._content = None
        super().__init__(parent)

    def render(self):
        surface = Theme.get("surface")
        border = Theme.get("border")

        header = tk.Frame(self._tk, bg=surface)
        header.pack(fill="x")

        self._body = tk.Frame(self._tk, bg=surface)
        self._body.pack(fill="both", expand=True, pady=(8, 0))

        for i, spec in enumerate(self.tabs_specs):
            btn = tk.Button(header, text=spec.get("text", f"Onglet {i + 1}"),
                            relief=tk.FLAT, bd=0, padx=16, pady=7,
                            cursor="hand2", font=Theme.font("base", "bold"),
                            command=lambda idx=i: self.select(idx))
            btn.pack(side="left", padx=(0, 4))
            self._tab_buttons[i] = btn

        if self.tabs_specs:
            self.select(0)

    def select(self, index):
        """Active l'onglet d'index `index`."""
        if not 0 <= index < len(self.tabs_specs):
            raise IndexError(f"Onglet invalide : {index}")
        if self._content is not None:
            self._content.destroy()
            self._content = None
        self._index = index
        spec = self.tabs_specs[index]
        self._content = self._build_content(spec.get("content"))
        self._apply_tab_styles()

    def _build_content(self, content):
        if content is None:
            return None
        if isinstance(content, type):
            return content(self._body)
        return content(self._body)

    @property
    def index(self):
        return self._index

    def _apply_tab_styles(self):
        if self._tk is None:
            return
        primary = Theme.get("primary")
        on_primary = Theme.get("on_primary")
        surface = Theme.get("surface")
        text = Theme.get("text")
        for i, btn in self._tab_buttons.items():
            active = i == self._index
            btn.configure(bg=primary if active else surface,
                          fg=on_primary if active else text,
                          activebackground=Theme.get("primary_hover") if active
                          else Theme.get("surface_hover"),
                          activeforeground=on_primary if active else text)

    def _apply_theme(self):
        if self._tk is not None:
            surface = Theme.get("surface")
            self._tk.configure(bg=surface)
            if self._body is not None:
                self._body.configure(bg=surface)
            self._apply_tab_styles()