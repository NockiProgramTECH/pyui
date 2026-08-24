"""Barre de progression PyUI (Niveau 1)."""

from tkinter import ttk

from pyui.core.component import Component


class ProgressBar(Component):
    """Barre de progression déterminée ou indéterminée.

    Exemple :
        ProgressBar(parent, value=50, maximum=100, mode="determinate")
    """

    _tk_class = ttk.Progressbar

    def __init__(self, parent=None, value=0, maximum=100, mode="determinate"):
        self._value = value
        self._maximum = maximum
        self._mode = mode
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "value": self._value,
            "maximum": self._maximum,
            "mode": self._mode,
            "style": "PyUI.TProgressbar",
            **super()._widget_kwargs(**kwargs),
        }

    def set(self, value):
        self._value = value
        if self._tk is not None:
            self._tk.configure(value=value)

    def advance(self, delta=1):
        self._value += delta
        if self._tk is not None:
            self._tk.step(delta)