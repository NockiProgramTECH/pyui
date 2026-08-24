"""Liste déroulante PyUI (ComboBox) (Niveau 1)."""

from tkinter import ttk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Select(Component):
    """Liste déroulante à choix unique.

    Exemple :
        Select(parent, options=["Option 1", "Option 2"], value="Option 1", command=on_select)
    """

    _tk_class = ttk.Combobox

    def __init__(self, parent=None, options=None, value=None, state="readonly",
                 command=None, width=20):
        self.options = list(options or [])
        self._value = value
        self.state = state
        self.command = command
        self.width = width
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "values": self.options,
            "state": self.state,
            "width": self.width,
            "font": Theme.font("base"),
            **super()._widget_kwargs(**kwargs),
        }

    def render(self):
        if self._value is not None and self._value in self.options:
            self._tk.set(self._value)
        if self.command is not None:
            self._tk.bind("<<ComboboxSelected>>", lambda e: self.command())

    def get(self):
        if self._tk is not None:
            return self._tk.get()
        return self._value

    def set(self, value):
        self._value = value
        if self._tk is not None:
            self._tk.set(value)