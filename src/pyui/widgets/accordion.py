"""Accordéon PyUI (Niveau 2) : sections repliables."""

import tkinter as tk

from pyui.core.component import Component
from pyui.icons.manager import IconManager
from pyui.theme.theme import Theme


class Accordion(Component):
    """Liste de sections dépliables/pliables.

    Exemple :
        Accordion(parent, sections=[
            {"title": "Général", "content": lambda p: Label(p, text="Contenu")},
            {"title": "Avancé", "content": AdvancedPanel},
        ])
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, sections=None):
        self.sections_specs = list(sections or [])
        self._items = []
        super().__init__(parent)

    def render(self):
        surface = Theme.get("surface")
        for i, spec in enumerate(self.sections_specs):
            title = spec.get("title", f"Section {i + 1}")
            content = spec.get("content")

            header = tk.Frame(self._tk, bg=surface, highlightthickness=1,
                              highlightbackground=Theme.get("border"))
            header.pack(fill="x", pady=(0, 6))

            chevron = tk.Label(header, text="\u25B8", bg=surface,
                               fg=Theme.get("muted"), font=Theme.font("base"),
                               cursor="hand2", padx=10)
            chevron.pack(side="right")

            title_label = tk.Label(header, text=title, bg=surface,
                                   fg=Theme.get("text"),
                                   font=Theme.font("base", "bold"),
                                   anchor="w", cursor="hand2", padx=10, pady=8)
            title_label.pack(side="left", fill="x", expand=True)

            body = tk.Frame(self._tk, bg=surface)
            item = {"header": header, "body": body, "expanded": False,
                    "chevron": chevron, "content_spec": content, "content": None}
            self._items.append(item)

            header.bind("<Button-1>", lambda e, it=item: self.toggle(self._items.index(it)))
            title_label.bind("<Button-1>", lambda e, it=item: self.toggle(self._items.index(it)))
            chevron.bind("<Button-1>", lambda e, it=item: self.toggle(self._items.index(it)))

    def toggle(self, index):
        """Déplie/replie la section d'index `index`."""
        item = self._items[index]
        if item["expanded"]:
            item["body"].pack_forget()
            if item["content"] is not None:
                item["content"].destroy()
                item["content"] = None
            item["chevron"].configure(text="\u25B8")
            item["expanded"] = False
        else:
            if item["content"] is None:
                item["content"] = self._build_content(item["content_spec"], item["body"])
            item["body"].pack(fill="x", pady=(0, 6))
            item["chevron"].configure(text="\u25BE")
            item["expanded"] = True

    def _build_content(self, content, body):
        if content is None:
            return None
        if isinstance(content, type):
            return content(body)
        return content(body)

    def _apply_theme(self):
        if self._tk is None:
            return
        surface = Theme.get("surface")
        border = Theme.get("border")
        self._tk.configure(bg=surface)
        for item in self._items:
            item["header"].configure(bg=surface, highlightbackground=border)
            for child in item["header"].winfo_children():
                child.configure(bg=surface)