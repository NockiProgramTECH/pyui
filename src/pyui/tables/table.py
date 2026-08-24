"""Table de données PyUI (Niveau 6, Phase 7).

Exemple :
    DataTable(
        parent,
        columns=[("name", "Nom"), ("email", "Email"), ("phone", "Téléphone")],
        data=users,
        searchable=True,
        paginate=True,
        on_double_click=open_user,
        on_delete=delete_user,
    )
"""

import csv
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from pyui.core.component import Component
from pyui.layouts.row import Row
from pyui.theme.theme import Theme
from pyui.widgets.button import Button
from pyui.widgets.input import Input
from pyui.widgets.label import Label

from pyui.tables.columns import Column


class DataTable(Component):
    """Tableau : affichage, tri, recherche, pagination, sélection, actions, export."""

    _tk_class = tk.Frame
    bg_token = "background"

    def __init__(self, parent=None, columns=None, data=None, searchable=True,
                 paginate=True, page_size=10, selectable=True, multi_select=False,
                 sortable=True, height=None, on_select=None, on_double_click=None,
                 on_edit=None, on_delete=None, row_actions=None, exportable=False,
                 empty_text="Aucune donnée"):
        if not columns:
            raise ValueError("DataTable nécessite au moins une colonne")
        self.columns = [c if isinstance(c, Column) else Column(*c) for c in columns]
        self._data = list(data or [])
        self.searchable = searchable
        self.paginate = paginate
        self.page_size = max(1, page_size)
        self.selectable = selectable
        self.multi_select = multi_select
        self.sortable = sortable
        self.height = height
        self.on_select = on_select
        self.on_double_click = on_double_click
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.row_actions = row_actions
        self.exportable = exportable
        self.empty_text = empty_text

        self._page = 1
        self._sort_key = None
        self._sort_reverse = False
        self._search_text = ""
        self._row_map = {}
        self._filter_predicate = None

        self._tree = None
        self._search_input = None
        self._page_label = None
        self._prev_button = None
        self._next_button = None
        self._filtered = []

        super().__init__(parent)

    # ------------------------------------------------------------------
    # Rendu
    # ------------------------------------------------------------------
    def render(self):
        if self.searchable:
            toolbar = Row(self, spacing=8)
            toolbar.pack(fill="x", pady=(0, 8))
            self._search_input = Input(toolbar, placeholder="Rechercher...", width=28)
            self._search_input.bind("<KeyRelease>", lambda e: self._on_search())
            if self.exportable:
                Button(toolbar, text="Exporter CSV", icon="download",
                       variant="secondary", command=self._export_dialog)

        body = tk.Frame(self._tk, bg=Theme.get(self.bg_token))
        body.pack(fill="both", expand=True)

        keys = [c.key for c in self.columns]
        selectmode = "none"
        if self.selectable:
            selectmode = "extended" if self.multi_select else "browse"

        self._tree = ttk.Treeview(body, columns=keys, show="headings",
                                  selectmode=selectmode, style="Treeview",
                                  height=self.height)
        self._tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(body, orient="vertical", command=self._tree.yview)
        vsb.pack(side="right", fill="y")
        hsb = ttk.Scrollbar(self._tk, orient="horizontal", command=self._tree.xview)
        hsb.pack(fill="x")
        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for col in self.columns:
            anchor = "center" if col.align == "center" else ("e" if col.align == "right" else "w")
            self._tree.column(col.key, width=col.width or 120, anchor=anchor, stretch=True)
            text = col.title
            command = (lambda c=col: self._toggle_sort(c.key)) if (self.sortable and col.sortable) else None
            self._tree.heading(col.key, text=text, command=command)

        if self.selectable:
            self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self._tree.bind("<Double-1>", self._on_double_click)
        self._tree.bind("<Button-3>", self._on_right_click)

        if self.paginate:
            pager = Row(self, spacing=8)
            pager.pack(fill="x", pady=(8, 0))
            self._prev_button = Button(pager, text="Précédent", icon="arrow-left",
                                       variant="ghost", command=self.previous_page)
            self._page_label = Label(pager, text="", color="muted", size="sm")
            self._next_button = Button(pager, text="Suivant", icon="arrow-right",
                                       variant="ghost", command=self.next_page)

        self.refresh()

    # ------------------------------------------------------------------
    # Données
    # ------------------------------------------------------------------
    def set_data(self, data):
        """Remplace les données du tableau."""
        self._data = list(data or [])
        self._page = 1
        self.refresh()
        return self

    def add_row(self, row):
        self._data.append(row)
        self.refresh()

    def update_row(self, predicate, row):
        for i, existing in enumerate(self._data):
            if predicate(existing):
                self._data[i] = row
                break
        self.refresh()

    def remove_row(self, predicate):
        self._data = [r for r in self._data if not predicate(r)]
        self.refresh()

    def clear(self):
        self._data = []
        self.refresh()

    @property
    def data(self):
        return self._data

    def set_filter(self, predicate):
        """Applique un filtre personnalisé (predicate row -> bool)."""
        self._filter_predicate = predicate
        self._page = 1
        self.refresh()

    def selected_rows(self):
        """Renvoie la ou les lignes sélectionnées (liste)."""
        if self._tree is None:
            return []
        return [self._row_map[iid] for iid in self._tree.selection() if iid in self._row_map]

    # ------------------------------------------------------------------
    # Affichage / tri / recherche
    # ------------------------------------------------------------------
    def _visible_data(self):
        data = self._data
        if self._filter_predicate is not None:
            data = [r for r in data if self._filter_predicate(r)]
        if self._search_text:
            terms = self._search_text.lower()
            data = [r for r in data if self._matches(r, terms)]
        if self._sort_key is not None:
            data = sorted(data, key=lambda r: str(r.get(self._sort_key, "")),
                          reverse=self._sort_reverse)
        self._filtered = data
        if self.paginate:
            total = len(data)
            page_count = max(1, (total + self.page_size - 1) // self.page_size)
            self._page = max(1, min(self._page, page_count))
            start = (self._page - 1) * self.page_size
            return data[start:start + self.page_size], page_count
        return data, 1

    def _matches(self, row, terms):
        for col in self.columns:
            if terms in str(row.get(col.key, "")).lower():
                return True
        return False

    def _toggle_sort(self, key):
        if self._sort_key == key:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_key = key
            self._sort_reverse = False
        self.refresh()

    def _on_search(self):
        self._search_text = self._search_input.get()
        self._page = 1
        self.refresh()

    def refresh(self):
        """Re-rend les lignes visibles et la barre de pagination."""
        if self._tree is None:
            return
        self._tree.delete(*self._tree.get_children())
        self._row_map = {}
        rows, page_count = self._visible_data()

        keys = [c.key for c in self.columns]
        for row in rows:
            values = [row.get(key, "") for key in keys]
            iid = self._tree.insert("", "end", values=values)
            self._row_map[iid] = row

        for col in self.columns:
            text = col.title
            if self._sort_key == col.key:
                text += " \u25B2" if not self._sort_reverse else " \u25BC"
            self._tree.heading(col.key, text=text)

        if self.paginate and self._page_label is not None:
            self._page_label.text = f"Page {self._page} / {page_count} — {len(self._filtered)} éléments"
            if self._prev_button is not None:
                if self._page <= 1:
                    self._prev_button.disable()
                else:
                    self._prev_button.enable()
            if self._next_button is not None:
                if self._page >= page_count:
                    self._next_button.disable()
                else:
                    self._next_button.enable()

    # ------------------------------------------------------------------
    # Pagination
    # ------------------------------------------------------------------
    def previous_page(self):
        if self._page > 1:
            self._page -= 1
            self.refresh()

    def next_page(self):
        self._page += 1
        self.refresh()

    # ------------------------------------------------------------------
    # Événements
    # ------------------------------------------------------------------
    def _on_tree_select(self, event):
        if self.on_select is not None:
            self.on_select(self.selected_rows())

    def _on_double_click(self, event):
        if self.on_double_click is None:
            return
        iid = self._tree.identify_row(event.y)
        if iid and iid in self._row_map:
            self.on_double_click(self._row_map[iid])

    def _on_right_click(self, event):
        iid = self._tree.identify_row(event.y)
        if not iid:
            return
        if self.selectable:
            self._tree.selection_set(iid)
        row = self._row_map[iid]
        menu = tk.Menu(self._tk, tearoff=0)
        menu.configure(bg=Theme.get("surface"), fg=Theme.get("text"),
                       activebackground=Theme.get("primary"),
                       activeforeground=Theme.get("on_primary"),
                       relief="flat", bd=1)
        if self.on_edit is not None:
            menu.add_command(label="Modifier", command=lambda: self.on_edit(row))
        if self.on_delete is not None:
            menu.add_command(label="Supprimer", command=lambda: self.on_delete(row))
        if self.row_actions is not None:
            if self.on_edit is not None or self.on_delete is not None:
                menu.add_separator()
            for label, command in self.row_actions(row):
                menu.add_command(label=label, command=command)
        if menu.index("end") is not None:
            menu.tk_popup(event.x_root, event.y_root)

    # ------------------------------------------------------------------
    # Export CSV
    # ------------------------------------------------------------------
    def _export_dialog(self):
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Fichier CSV", "*.csv")],
            initialfile=f"export_{datetime.now():%Y%m%d_%H%M%S}.csv",
        )
        if filename:
            self.export(filename)

    def export(self, filename=None):
        """Exporte les données en CSV (séparateur ;, encodage UTF-8 BOM)."""
        filename = filename or f"export_{datetime.now():%Y%m%d_%H%M%S}.csv"
        with open(filename, "w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.writer(fh, delimiter=";")
            writer.writerow([col.title for col in self.columns])
            for row in self._data:
                writer.writerow([row.get(col.key, "") for col in self.columns])
        return filename

    # ------------------------------------------------------------------
    # Thème
    # ------------------------------------------------------------------
    def _apply_theme(self):
        if self._tk is not None:
            self._tk.configure(bg=Theme.get(self.bg_token))