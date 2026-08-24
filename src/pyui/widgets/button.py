"""Bouton PyUI avec styles, variantes et icônes (Niveau 1)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.icons.manager import IconManager
from pyui.theme.theme import Theme


class Button(Component):
    """Bouton cliquable avec variantes et hover.

    Exemple :
        Button(parent, text="Enregistrer", command=save, variant="primary", icon="save")
    """

    _tk_class = tk.Button

    _VARIANTS = {
        "primary":   {"bg": "primary",   "fg": "on_primary",   "hover": "primary_hover"},
        "secondary": {"bg": "secondary", "fg": "on_secondary", "hover": "secondary_hover"},
        "success":   {"bg": "success",   "fg": "on_success",   "hover": "success_hover"},
        "danger":    {"bg": "danger",    "fg": "on_danger",    "hover": "danger_hover"},
        "warning":   {"bg": "warning",   "fg": "on_warning",   "hover": "warning_hover"},
        "ghost":     {"bg": "surface",   "fg": "text",         "hover": "surface_hover"},
        "outline":   {"bg": "surface",   "fg": "primary",      "hover": "surface_hover"},
    }

    def __init__(self, parent=None, text="", command=None, variant="primary",
                 icon=None, disabled=False, width=None):
        self._text = text
        self.command = command
        self.variant = variant
        self.icon = icon
        self.disabled = disabled
        self.width = width
        self._hover_bound = False
        self._hover_color = None
        super().__init__(parent)

    def _resolved_text(self):
        if not self.icon:
            return self._text
        glyph = IconManager.glyph(self.icon)
        if not glyph:
            return self._text
        return f"{glyph}  {self._text}" if self._text else glyph

    def _widget_kwargs(self, **kwargs):
        return {
            "text": self._resolved_text(),
            "command": self.command,
            "relief": tk.FLAT,
            "borderwidth": 0,
            "padx": 14,
            "pady": 6,
            "cursor": "hand2",
            "font": Theme.font("base", "bold"),
            "width": self.width,
            "state": "disabled" if self.disabled else "normal",
            **super()._widget_kwargs(**kwargs),
        }

    def _apply_theme(self):
        if self._tk is None:
            return
        v = self._VARIANTS.get(self.variant, self._VARIANTS["primary"])
        bg = Theme.get(v["bg"])
        fg = Theme.get(v["fg"])
        self._hover_color = Theme.get(v["hover"])
        self._tk.configure(
            bg=bg, fg=fg,
            activebackground=self._hover_color,
            activeforeground=fg,
            disabledforeground=Theme.get("muted"),
        )
        if not self._hover_bound:
            self.bind("<Enter>", lambda e: self._on_enter())
            self.bind("<Leave>", lambda e: self._on_leave())
            self._hover_bound = True

    def _on_enter(self):
        if self._tk is not None and self._tk.cget("state") != "disabled":
            self._tk.configure(bg=self._hover_color)

    def _on_leave(self):
        if self._tk is not None and self._tk.cget("state") != "disabled":
            v = self._VARIANTS.get(self.variant, self._VARIANTS["primary"])
            self._tk.configure(bg=Theme.get(v["bg"]))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        if self._tk is not None:
            self._tk.configure(text=value)

    def enable(self):
        """Active le bouton."""
        self.disabled = False
        if self._tk is not None:
            self._tk.configure(state="normal")

    def disable(self):
        """Désactive le bouton."""
        self.disabled = True
        if self._tk is not None:
            self._tk.configure(state="disabled")