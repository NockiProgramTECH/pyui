"""Fenêtre modale PyUI (Niveau 2).

Exemple :
    modal = Modal(app, title="Confirmer", content=ConfirmPanel)
    modal.open()
"""

import tkinter as tk

from pyui.theme.theme import Theme
from pyui.widgets.button import Button


class Modal:
    """Fenêtre modale avec titre, contenu personnalisé et fermeture."""

    def __init__(self, parent=None, title="", content=None, on_close=None, size=None):
        self.parent = parent
        self.title = title
        self.content_spec = content
        self.on_close = on_close
        self.size = size
        self._win = None
        self._body = None
        self._content = None

    # ------------------------------------------------------------------
    def open(self):
        """Ouvre la fenêtre modale (bloquante sur l'application)."""
        root = self.parent.tk if self.parent is not None else tk._default_root
        if root is None:
            return None
        surface = Theme.get("surface")
        border = Theme.get("border")
        text = Theme.get("text")

        win = tk.Toplevel(root)
        win.title(self.title)
        win.configure(bg=surface)
        win.transient(root)
        win.grab_set()
        if self.size:
            win.geometry(f"{self.size[0]}x{self.size[1]}")
        win.resizable(False, False)
        self._win = win

        if self.title:
            header = tk.Frame(win, bg=surface, highlightthickness=1,
                              highlightbackground=border)
            header.pack(fill="x")
            tk.Label(header, text=self.title, bg=surface, fg=text,
                     font=Theme.font("lg", "bold"), padx=14, pady=10,
                     anchor="w").pack(side="left", fill="x", expand=True)
            close = tk.Label(header, text="\u00D7", bg=surface, fg=text,
                             font=Theme.font("xl", "bold"), cursor="hand2",
                             padx=14)
            close.pack(side="right")
            close.bind("<Button-1>", lambda e: self.close())

        self._body = tk.Frame(win, bg=surface)
        self._body.pack(fill="both", expand=True, padx=14, pady=12)

        if self.content_spec is not None:
            self._content = self._build_content()

        win.protocol("WM_DELETE_WINDOW", self.close)
        win.update_idletasks()
        x = root.winfo_rootx() + (root.winfo_width() - win.winfo_width()) // 2
        y = root.winfo_rooty() + (root.winfo_height() - win.winfo_height()) // 3
        win.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        return win

    def _build_content(self):
        spec = self.content_spec
        if isinstance(spec, type):
            return spec(self._body)
        return spec(self._body)

    def close(self):
        """Ferme la fenêtre modale."""
        if self._win is not None and self._win.winfo_exists():
            try:
                self._win.grab_release()
            except tk.TclError:
                pass
            self._win.destroy()
        self._win = None
        if self.on_close is not None:
            self.on_close()

    def wait(self):
        """Bloque l'exécution jusqu'à la fermeture de la fenêtre."""
        if self._win is not None:
            self._win.wait_window()