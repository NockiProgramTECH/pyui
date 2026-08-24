"""Barre de navigation supérieure PyUI (Phase 4).

Exemple :
    Navbar(right, title="Dashboard", actions=[
        {"text": "Mode sombre", "icon": "settings", "variant": "ghost", "command": toggle_theme},
        {"icon": "bell", "variant": "ghost"},
    ])
"""

import tkinter as tk

from pyui.core.component import Component
from pyui.icons.manager import IconManager
from pyui.theme.theme import Theme
from pyui.widgets.button import Button
from pyui.widgets.label import Label


class Navbar(Component):
    """Barre horizontale : titre à gauche, actions à droite."""

    _tk_class = tk.Frame
    bg_token = "surface"

    def __init__(self, parent=None, title="", actions=None, height=56):
        self.nav_title = title
        self.actions = list(actions or [])
        self.height = height
        self._action_buttons = []
        super().__init__(parent)
        self.pack(fill="x", side="top")

    def _widget_kwargs(self, **kwargs):
        return {
            "height": self.height,
            "highlightthickness": 1,
            "highlightbackground": Theme.get("border"),
            "bd": 0,
            **super()._widget_kwargs(**kwargs),
        }

    def render(self):
        if self.nav_title:
            self._title_label = Label(self, text=self.nav_title, size="lg", weight="bold")
            self._title_label.pack(side="left", padx=16, pady=10)

        self._action_buttons = []
        for action in reversed(self.actions):
            btn = Button(
                self,
                text=action.get("text", ""),
                icon=action.get("icon"),
                command=action.get("command"),
                variant=action.get("variant", "ghost"),
                width=action.get("width"),
            )
            btn.pack(side="right", padx=(0, 8), pady=10)
            self._action_buttons.append(btn)

    def set_title(self, title):
        """Met à jour le titre affiché."""
        self.nav_title = title
        if getattr(self, "_title_label", None) is not None:
            self._title_label.text = title

    def _apply_theme(self):
        if self._tk is not None:
            self._tk.configure(bg=Theme.get("surface"),
                               highlightbackground=Theme.get("border"))