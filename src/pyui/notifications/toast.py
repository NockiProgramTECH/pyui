"""Notifications toast PyUI (Niveau 10).

Exemple :
    Toast.success("Client enregistré")
    Toast.error("Erreur de connexion")
"""

import tkinter as tk

from pyui.theme.theme import Theme

_VARIANTS = {
    "success": {"bg": "success", "fg": "on_success"},
    "error":   {"bg": "danger",  "fg": "on_danger"},
    "warning": {"bg": "warning", "fg": "on_warning"},
    "info":    {"bg": "primary", "fg": "on_primary"},
}


class Toast:
    """Notification éphémère affichée en bas à droite de la fenêtre."""

    _DURATION = 3500
    _active = []

    @classmethod
    def success(cls, message, duration=None):
        cls._show(message, "success", duration)

    @classmethod
    def error(cls, message, duration=None):
        cls._show(message, "error", duration)

    @classmethod
    def warning(cls, message, duration=None):
        cls._show(message, "warning", duration)

    @classmethod
    def info(cls, message, duration=None):
        cls._show(message, "info", duration)

    @classmethod
    def _show(cls, message, variant, duration):
        root = tk._default_root
        if root is None:
            return
        v = _VARIANTS.get(variant, _VARIANTS["info"])
        bg = Theme.get(v["bg"])
        fg = Theme.get(v["fg"])

        win = tk.Toplevel(root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.configure(bg=bg)
        win.bind("<Button-1>", lambda e: win.destroy())

        tk.Label(win, text=message, bg=bg, fg=fg,
                 font=Theme.font("base", "bold"), padx=18, pady=10,
                 cursor="hand2").pack()

        win.update_idletasks()
        x = root.winfo_rootx() + root.winfo_width() - win.winfo_width() - 24
        y = root.winfo_rooty() + root.winfo_height() - win.winfo_height() - 24
        win.geometry(f"+{x}+{y}")

        cls._active.append(win)
        ms = duration or cls._DURATION
        win.after(ms, lambda: cls._dismiss(win))

    @classmethod
    def _dismiss(cls, win):
        if win in cls._active:
            cls._active.remove(win)
        if win.winfo_exists():
            win.destroy()