"""Boîtes de dialogue standard PyUI (Niveau 10).

Exemple :
    Dialog.confirm("Voulez-vous supprimer ce client ?", on_confirm=delete_client)
    Dialog.error("Impossible de connecter la base de données")
"""

import tkinter as tk
from tkinter import messagebox

from pyui.theme.theme import Theme
from pyui.widgets.button import Button
from pyui.widgets.label import Label


class Dialog:
    """Fenêtres de dialogue standard (confirm, erreur, succès, avertissement...)."""

    @staticmethod
    def confirm(message, on_confirm=None, on_cancel=None, title="Confirmation",
                parent=None):
        """Ouvre un dialogue Oui/Non avec callbacks.

        Appels : on_confirm() si Oui, on_cancel() si Non.
        """
        Dialog._build(
            title=title, message=message,
            actions=[("Oui", True), ("Non", False)],
            on_result=on_confirm, on_cancel=on_cancel, parent=parent,
        )

    @staticmethod
    def info(message, title="Information", parent=None):
        messagebox.showinfo(title, message, parent=parent or tk._default_root)

    @staticmethod
    def error(message, title="Erreur", parent=None):
        messagebox.showerror(title, message, parent=parent or tk._default_root)

    @staticmethod
    def warning(message, title="Avertissement", parent=None):
        messagebox.showwarning(title, message, parent=parent or tk._default_root)

    @staticmethod
    def success(message, title="Succès", parent=None):
        messagebox.showinfo(title, message, parent=parent or tk._default_root)

    @staticmethod
    def _build(title, message, actions, on_result, on_cancel, parent):
        root = parent or tk._default_root
        if root is None:
            return None
        surface = Theme.get("surface")
        text = Theme.get("text")
        border = Theme.get("border")

        win = tk.Toplevel(root)
        win.title(title)
        win.configure(bg=surface)
        win.resizable(False, False)
        win.transient(root)
        win.grab_set()

        message_label = tk.Label(win, text=message, bg=surface, fg=text,
                                 font=Theme.font("base"), wraplength=380,
                                 justify="left")
        message_label.pack(fill="x", padx=20, pady=(20, 16))

        buttons = tk.Frame(win, bg=surface)
        buttons.pack(pady=(0, 14))

        def run(callback):
            def handler():
                win.destroy()
                if callback is not None:
                    callback()
            return handler

        first = True
        for label, result in actions:
            variant = "primary" if first else "ghost"
            btn = tk.Button(buttons, text=label, bg=Theme.get("primary"),
                            fg=Theme.get("on_primary"),
                            activebackground=Theme.get("primary_hover"),
                            activeforeground=Theme.get("on_primary"),
                            relief=tk.FLAT, bd=0, padx=18, pady=5,
                            cursor="hand2", font=Theme.font("base", "bold"),
                            command=run(on_result if result else on_cancel))
            btn.pack(side="left", padx=5)
            first = False

        win.protocol("WM_DELETE_WINDOW", run(on_cancel))
        win.update_idletasks()
        x = root.winfo_rootx() + (root.winfo_width() - win.winfo_width()) // 2
        y = root.winfo_rooty() + (root.winfo_height() - win.winfo_height()) // 3
        win.geometry(f"+{x}+{y}")
        win.wait_window()
        return win


class ConfirmDialog(Dialog):
    """Dialogue Oui/Non (alias de Dialog.confirm)."""

    @staticmethod
    def ask(message, on_confirm=None, on_cancel=None, title="Confirmation"):
        Dialog.confirm(message, on_confirm=on_confirm, on_cancel=on_cancel, title=title)


class ErrorDialog(Dialog):
    """Dialogue d'erreur (alias de Dialog.error)."""

    @staticmethod
    def show(message, title="Erreur"):
        Dialog.error(message, title=title)


class SuccessDialog(Dialog):
    """Dialogue de succès (alias de Dialog.success)."""

    @staticmethod
    def show(message, title="Succès"):
        Dialog.success(message, title=title)


class WarningDialog(Dialog):
    """Dialogue d'avertissement (alias de Dialog.warning)."""

    @staticmethod
    def show(message, title="Avertissement"):
        Dialog.warning(message, title=title)