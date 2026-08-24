"""Design System PyUI (Niveau 7-8).

Exemple :
    Theme.configure(primary="#2563EB", secondary="#64748B")
    Theme.set_mode("dark")
    Theme.dark()
    Theme.light()
"""

import tkinter as tk
from tkinter import ttk

from pyui.theme.colors import LIGHT, DARK
from pyui.theme.typography import DEFAULT_FONT, SIZES, WEIGHTS


class Theme:
    """Configuration globale des couleurs, typographie et styles.

    Singleton par classe : les composants s'abonnent via Theme.subscribe()
    et sont automatiquement actualisés à chaque changement.
    """

    _mode = "light"
    _tokens = dict(LIGHT)
    _subscribers = []
    _font_family = DEFAULT_FONT

    # ------------------------------------------------------------------
    # Jetons de design
    # ------------------------------------------------------------------
    @classmethod
    def configure(cls, **tokens):
        """Définit ou surcharge des jetons (couleurs, rayon, espacements...)."""
        cls._tokens.update(tokens)
        cls._apply()
        return cls

    @classmethod
    def get(cls, token, default=None):
        """Renvoie la valeur du jeton (ex : Theme.get("primary"))."""
        return cls._tokens.get(token, default)

    @classmethod
    def font(cls, size="base", weight="normal"):
        """Renvoie une police Tkinter : (famille, taille, graisse)."""
        return (cls._font_family, SIZES.get(size, SIZES["base"]),
                WEIGHTS.get(weight, "normal"))

    # ------------------------------------------------------------------
    # Modes clair / sombre
    # ------------------------------------------------------------------
    @classmethod
    def set_mode(cls, mode):
        """Bascule entre "light" et "dark" et actualise tous les composants."""
        if mode not in ("light", "dark"):
            raise ValueError(f"Mode inconnu : {mode!r}")
        cls._mode = mode
        cls._tokens = dict(LIGHT if mode == "light" else DARK)
        cls._apply()

    @classmethod
    def light(cls):
        cls.set_mode("light")

    @classmethod
    def dark(cls):
        cls.set_mode("dark")

    @classmethod
    def mode(cls):
        return cls._mode

    # ------------------------------------------------------------------
    # Abonnés (composants)
    # ------------------------------------------------------------------
    @classmethod
    def subscribe(cls, callback):
        """Abonne un callback appelé à chaque changement de thème.

        Renvoie une fonction de désabonnement.
        """
        cls._subscribers.append(callback)

        def unsubscribe():
            if callback in cls._subscribers:
                cls._subscribers.remove(callback)

        return unsubscribe

    @classmethod
    def _apply(cls):
        cls._setup_ttk()
        for callback in list(cls._subscribers):
            callback()

    @classmethod
    def _setup_ttk(cls):
        """Applique les couleurs aux widgets ttk (Combobox, Progressbar...)."""
        try:
            style = ttk.Style()
            style.theme_use("clam")
            surface = cls.get("surface")
            text = cls.get("text")
            border = cls.get("border")
            primary = cls.get("primary")

            style.configure("TCombobox",
                            fieldbackground=surface, background=surface,
                            foreground=text, arrowcolor=text,
                            bordercolor=border, lightcolor=border, darkcolor=border,
                            padding=4)
            style.map("TCombobox",
                      fieldbackground=[("readonly", surface)],
                      foreground=[("readonly", text)])

            style.configure("PyUI.TProgressbar", background=primary,
                            troughcolor=border, bordercolor=border)
            style.layout("Horizontal.PyUI.TProgressbar",
                         style.layout("Horizontal.TProgressbar"))
            style.layout("Vertical.PyUI.TProgressbar",
                         style.layout("Vertical.TProgressbar"))

            style.configure("Treeview",
                            background=surface, fieldbackground=surface,
                            foreground=text, borderwidth=0, rowheight=28)
            style.map("Treeview",
                      background=[("selected", primary)],
                      foreground=[("selected", cls.get("on_primary"))])
            style.configure("Treeview.Heading",
                            background=border, foreground=text,
                            relief="flat", padding=6)
            style.map("Treeview.Heading",
                      background=[("active", cls.get("surface_hover"))])
            style.configure("Treeview.Scrollbar", troughcolor=border)
            style.configure("TSeparator", background=border)

            root = tk._default_root
            if root is not None:
                root.option_add("*TCombobox*Listbox.background", surface)
                root.option_add("*TCombobox*Listbox.foreground", text)
                root.option_add("*TCombobox*Listbox.selectBackground", primary)
                root.option_add("*TCombobox*Listbox.selectForeground", cls.get("on_primary"))
        except Exception:
            pass
