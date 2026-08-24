"""Chargement PyUI (Niveau 2) : surcouche avec spinner et message."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme
from pyui.widgets.label import Label
from pyui.widgets.spinner import Spinner


class Loading(Component):
    """Surcouche de chargement affichée pendant une opération.

    Exemple :
        loading = Loading(app, message="Chargement...")
        loading.open()
        # ... opération ...
        loading.close()
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, message="Chargement...", spinner_size=32):
        self.loading_message = message
        self.spinner_size = spinner_size
        self._spinner = None
        super().__init__(parent)

    def render(self):
        container = tk.Frame(self._tk, bg=Theme.get(self.bg_token))
        container.pack(expand=True)
        self._spinner = Spinner(container, size=self.spinner_size)
        self._spinner.start()
        Label(container, text=self.loading_message, color="muted", size="sm").pack(pady=(8, 0))

    def _apply_theme(self):
        if self._tk is not None:
            bg = Theme.get(self.bg_token)
            self._tk.configure(bg=bg)
            for child in self._tk.winfo_children():
                child.configure(bg=bg)

    def open(self):
        """Affiche la surcouche par-dessus le contenu."""
        self.show()
        if self._tk is not None:
            self._tk.lift()
        return self

    def close(self):
        """Masque la surcouche."""
        self.hide()
        return self

    def destroy(self):
        if self._spinner is not None:
            self._spinner.stop()
        super().destroy()