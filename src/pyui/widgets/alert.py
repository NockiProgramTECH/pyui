"""Alerte PyUI (Niveau 2) : message avec variante et fermeture optionnelle."""

import tkinter as tk

from pyui.core.component import Component
from pyui.icons.manager import IconManager
from pyui.theme.theme import Theme


class Alert(Component):
    """Alerte colorée : info, success, warning, danger.

    Exemple :
        Alert(parent, message="Client enregistré", variant="success", dismissible=True)
    """

    _tk_class = tk.Frame

    _VARIANTS = {
        "info":    {"bg": "primary",   "fg": "on_primary",   "icon": "info"},
        "success": {"bg": "success",   "fg": "on_success",   "icon": "check"},
        "warning": {"bg": "warning",   "fg": "on_warning",   "icon": "warning"},
        "danger":  {"bg": "danger",    "fg": "on_danger",    "icon": "delete"},
    }

    def __init__(self, parent=None, message="", variant="info", dismissible=False,
                 icon=None):
        self.message = message
        self.variant = variant
        self.dismissible = dismissible
        self.alert_icon = icon
        self._label = None
        super().__init__(parent)

    def render(self):
        v = self._VARIANTS.get(self.variant, self._VARIANTS["info"])
        bg = Theme.get(v["bg"])
        fg = Theme.get(v["fg"])
        icon = self.alert_icon or v["icon"]

        glyph = IconManager.glyph(icon)
        prefix = f"{glyph}  " if glyph else ""
        self._label = tk.Label(self._tk, text=prefix + self.message, bg=bg, fg=fg,
                               font=Theme.font("base"), justify="left", anchor="w",
                               padx=12, pady=8)
        self._label.pack(side="left", fill="x", expand=True)

        if self.dismissible:
            close = tk.Label(self._tk, text="\u00D7", bg=bg, fg=fg,
                             font=Theme.font("lg", "bold"), cursor="hand2",
                             padx=4, pady=4)
            close.pack(side="right", padx=(0, 6))
            close.bind("<Button-1>", lambda e: self.hide())

    def _apply_theme(self):
        if self._tk is None:
            return
        v = self._VARIANTS.get(self.variant, self._VARIANTS["info"])
        bg = Theme.get(v["bg"])
        fg = Theme.get(v["fg"])
        self._tk.configure(bg=bg)
        for child in self._tk.winfo_children():
            child.configure(bg=bg, fg=fg)