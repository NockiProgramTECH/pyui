"""Barre latérale PyUI (Niveau 3, Phase 4).

Exemple :
    Sidebar(
        app,
        title="Gestion",
        items=[
            {"key": "dashboard", "text": "Dashboard", "icon": "home", "route": "/"},
            {"text": "Ventes", "icon": "chart", "children": [
                {"text": "Nouvelles ventes", "route": "/ventes/nouvelle"},
                {"text": "Historique", "route": "/ventes/historique"},
            ]},
        ],
        app=app,
    )
"""

import tkinter as tk
from tkinter import ttk

from pyui.core.component import Component
from pyui.icons.manager import IconManager
from pyui.theme.theme import Theme


class Sidebar(Component):
    """Menu latéral : titre, logo, items, icônes, sous-menus, élément actif, routes."""

    _tk_class = tk.Frame
    bg_token = "surface"

    def __init__(self, parent=None, items=None, title=None, logo=None, width=240,
                 position="left", active=None, app=None, on_select=None):
        self.items = list(items or [])
        self.sidebar_title = title
        self.logo = logo
        self.width = width
        self.position = position if position in ("left", "right") else "left"
        self.active_key = active
        self.app = app
        self.on_select = on_select
        self._rows = []
        self._collapsed = False
        self._nav_bound = False
        super().__init__(parent)
        self.pack(side=self.position, fill="y")

    def _widget_kwargs(self, **kwargs):
        return {
            "width": self.width,
            "highlightthickness": 1,
            "highlightbackground": Theme.get("border"),
            "bd": 0,
            **super()._widget_kwargs(**kwargs),
        }

    # ------------------------------------------------------------------
    # Rendu
    # ------------------------------------------------------------------
    def render(self):
        self._rows = []
        surface = Theme.get("surface")

        if self.logo or self.sidebar_title:
            header = tk.Frame(self._tk, bg=surface)
            header.pack(fill="x", padx=14, pady=(14, 10))
            if self.logo:
                tk.Label(header, text=self.logo, bg=surface,
                         fg=Theme.get("primary"),
                         font=("Segoe UI Emoji", 16)).pack(side="left")
            if self.sidebar_title:
                tk.Label(header, text=self.sidebar_title, bg=surface,
                         fg=Theme.get("text"),
                         font=Theme.font("lg", "bold")).pack(side="left", padx=(8, 0))
            self._header = header

        ttk.Separator(self._tk, orient="horizontal").pack(fill="x", pady=8)

        for item in self.items:
            self._render_item(item, self._tk, level=0)

        spacer = tk.Frame(self._tk, bg=surface)
        spacer.pack(fill="both", expand=True)

        if self.app is not None and not self._nav_bound:
            self.app.events.on("navigate", self._on_navigate)
            self._nav_bound = True

    def _render_item(self, item, parent, level):
        key = str(item.get("key", item.get("text", "")))
        text = item.get("text", "")
        glyph = IconManager.glyph(item.get("icon", ""))
        label = f"{glyph}  {text}" if glyph else text

        container = tk.Frame(parent, bg=Theme.get("surface"))
        container.pack(fill="x", padx=8, pady=1)

        chevron = None
        children = item.get("children")
        child_rows = []

        if children:
            chevron = tk.Label(container, text="\u25B8", bg=Theme.get("surface"),
                               fg=Theme.get("muted"), font=Theme.font("base"))
            chevron.pack(side="right", padx=(0, 6))

        button = tk.Button(container, text=label, anchor="w", relief=tk.FLAT,
                           bd=0, padx=12, pady=7, font=Theme.font("base"),
                           cursor="hand2", bg=Theme.get("surface"),
                           fg=Theme.get("text"),
                           highlightthickness=0)
        button.pack(side="left", fill="x", expand=True)

        row = {
            "key": key,
            "item": item,
            "container": container,
            "button": button,
            "chevron": chevron,
            "children_frame": None,
            "child_rows": child_rows,
            "expanded": False,
        }
        button.configure(command=lambda r=row: self._on_click(r))
        button.bind("<Enter>", lambda e, r=row: self._on_hover(r, enter=True))
        button.bind("<Leave>", lambda e, r=row: self._on_hover(r, enter=False))

        self._rows.append(row)

        if children:
            children_frame = tk.Frame(parent, bg=Theme.get("surface"))
            row["children_frame"] = children_frame
            for child in children:
                child_rows.append(self._render_item(child, children_frame, level=level + 1))

        return row

    def _on_hover(self, row, enter):
        if self._tk is None:
            return
        is_active = row["key"] == self.active_key
        if enter:
            color = Theme.get("primary_hover") if is_active else Theme.get("surface_hover")
        else:
            color = Theme.get("primary") if is_active else Theme.get("surface")
        row["button"].configure(bg=color)

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------
    def _on_click(self, row):
        item = row["item"]
        if row["child_rows"]:
            self._toggle(row)
            return
        self.set_active(row["key"])
        if self.on_select is not None:
            self.on_select(item)
        command = item.get("command")
        if command is not None:
            command()
        route = item.get("route")
        if route and self.app is not None:
            self.app.navigate(route)

    def _toggle(self, row):
        if row["expanded"]:
            row["children_frame"].pack_forget()
            row["expanded"] = False
            if row["chevron"] is not None:
                row["chevron"].configure(text="\u25B8")
        else:
            row["children_frame"].pack(fill="x", padx=8)
            row["expanded"] = True
            if row["chevron"] is not None:
                row["chevron"].configure(text="\u25BE")

    def set_active(self, key):
        """Définit l'élément actif (mis en surbrillance)."""
        self.active_key = str(key)
        self._apply_row_styles()

    @property
    def active(self):
        return self.active_key

    def _apply_row_styles(self):
        for row in self._rows:
            is_active = row["key"] == self.active_key
            row["button"].configure(
                bg=Theme.get("primary") if is_active else Theme.get("surface"),
                fg=Theme.get("on_primary") if is_active else Theme.get("text"),
            )
            if row["chevron"] is not None:
                row["chevron"].configure(bg=Theme.get("surface"), fg=Theme.get("muted"))

    # ------------------------------------------------------------------
    # Navigation intégrée
    # ------------------------------------------------------------------
    def _on_navigate(self, event):
        path = event.data.get("path")
        self._activate_route(path)

    def _activate_route(self, path, rows=None, ancestors=None):
        rows = self._rows if rows is None else rows
        for row in rows:
            if row["item"].get("route") == path:
                for ancestor in reversed(ancestors or []):
                    if not ancestor["expanded"]:
                        self._toggle(ancestor)
                self.set_active(row["key"])
                return True
            if self._activate_route(path, row["child_rows"], (ancestors or []) + [row]):
                return True
        return False

    # ------------------------------------------------------------------
    # Repli / déploiement
    # ------------------------------------------------------------------
    def collapse(self, animated=False):
        """Replie la sidebar (voir Niveau 18 — Animations)."""
        self._collapsed = True
        if self._tk is not None:
            self._tk.pack_forget()

    def expand(self, animated=False):
        """Déplie la sidebar."""
        self._collapsed = False
        if self._tk is not None:
            self._tk.pack(side=self.position, fill="y")

    @property
    def collapsed(self):
        return self._collapsed

    # ------------------------------------------------------------------
    # Destruction : désabonnement du bus d'événements
    # ------------------------------------------------------------------
    def destroy(self):
        if self._nav_bound and self.app is not None:
            self.app.events.off("navigate", self._on_navigate)
            self._nav_bound = False
        super().destroy()

    # ------------------------------------------------------------------
    # Thème
    # ------------------------------------------------------------------
    def _apply_theme(self):
        if self._tk is None:
            return
        surface = Theme.get("surface")
        self._tk.configure(bg=surface, highlightbackground=Theme.get("border"))
        if hasattr(self, "_header"):
            for child in self._header.winfo_children():
                child.configure(bg=surface)
        for row in self._rows:
            row["container"].configure(bg=surface)
            if row["children_frame"] is not None:
                row["children_frame"].configure(bg=surface)
        self._apply_row_styles()