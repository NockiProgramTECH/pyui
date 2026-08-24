"""Infobulle PyUI (Niveau 2)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Tooltip(Component):
    """Infobulle affichée au survol d'un composant.

    Exemple :
        Tooltip(button, text="Enregistrer les modifications", delay=400)
    """

    _tk_class = tk.Toplevel

    def __init__(self, widget, text="", delay=400):
        self.widget = widget
        self.tooltip_text = text
        self.delay = delay
        self._win = None
        self._after_id = None
        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")
        widget.bind("<Motion>", self._on_motion, add="+")

    # ------------------------------------------------------------------
    def _on_enter(self, event):
        self._cancel()
        self._after_id = self.widget._tk.after(self.delay, self._show)

    def _on_leave(self, event):
        self._cancel()
        self._hide()

    def _on_motion(self, event):
        if self._win is not None and self._win.winfo_exists():
            x = event.x_root + 12
            y = event.y_root + 12
            self._win.geometry(f"+{x}+{y}")

    def _cancel(self):
        if self._after_id is not None and self.widget._tk is not None:
            try:
                self.widget._tk.after_cancel(self._after_id)
            except tk.TclError:
                pass
            self._after_id = None

    def _show(self):
        self._after_id = None
        root = self.widget._tk.winfo_toplevel()
        surface = Theme.get("surface")
        text = Theme.get("text")
        border = Theme.get("border")

        self._win = tk.Toplevel(root)
        self._win.overrideredirect(True)
        self._win.configure(bg=border)
        tk.Label(self._win, text=self.tooltip_text, bg=surface, fg=text,
                 font=Theme.font("sm"), padx=8, pady=4).pack(padx=1, pady=1)
        x = root.winfo_pointerx() + 12
        y = root.winfo_pointery() + 12
        self._win.geometry(f"+{x}+{y}")
        self._win.attributes("-topmost", True)

    def _hide(self):
        if self._win is not None:
            try:
                self._win.destroy()
            except tk.TclError:
                pass
            self._win = None

    def destroy(self):
        self._cancel()
        self._hide()