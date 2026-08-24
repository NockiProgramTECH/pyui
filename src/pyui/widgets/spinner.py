"""Spinner PyUI (Niveau 2) : animation de chargement sur Canvas."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Spinner(Component):
    """Spinner animé (indéterminé).

    Exemple :
        Spinner(parent, size=28, color="primary").start()
    """

    _tk_class = tk.Canvas

    def __init__(self, parent=None, size=24, color="primary", speed=60):
        self.size = size
        self._color_token = color
        self.speed = speed
        self._angle = 0
        self._after_id = None
        self._running = False
        self._color = None
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "width": self.size,
            "height": self.size,
            "bg": Theme.get(getattr(self.parent, "bg_token", "background")),
            "highlightthickness": 0,
            "bd": 0,
            **super()._widget_kwargs(**kwargs),
        }

    def _apply_theme(self):
        if self._tk is None:
            return
        self._color = Theme.get(self._color_token, Theme.get("primary"))
        parent_bg = Theme.get(getattr(self.parent, "bg_token", "background"))
        self._tk.configure(bg=parent_bg)
        if self._running:
            self._draw()

    # ------------------------------------------------------------------
    def start(self):
        """Démarre l'animation."""
        if self._running or self._tk is None:
            return
        self._running = True
        self._tick()

    def stop(self):
        """Arrête l'animation."""
        self._running = False
        if self._after_id is not None and self._tk is not None:
            try:
                self._tk.after_cancel(self._after_id)
            except tk.TclError:
                pass
            self._after_id = None

    def _tick(self):
        if not self._running or self._tk is None:
            return
        self._draw()
        self._angle = (self._angle + 30) % 360
        self._after_id = self._tk.after(self.speed, self._tick)

    def _draw(self):
        if self._tk is None:
            return
        self._tk.delete("all")
        s = self.size
        color = self._color or Theme.get("primary")
        for i in range(8):
            start = self._angle + i * 45
            self._tk.create_arc(3, 3, s - 3, s - 3,
                                start=start, extent=25,
                                outline=color, width=3, style="arc")