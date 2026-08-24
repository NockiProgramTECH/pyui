"""Séparateur PyUI (Niveau 1)."""

from tkinter import ttk

from pyui.core.component import Component


class Separator(Component):
    """Ligne de séparation visuelle horizontale ou verticale.

    Exemple :
        Separator(parent, orientation="horizontal")
    """

    _tk_class = ttk.Separator

    def __init__(self, parent=None, orientation="horizontal"):
        self._orient = "horizontal" if orientation == "horizontal" else "vertical"
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {"orient": self._orient, **super()._widget_kwargs(**kwargs)}