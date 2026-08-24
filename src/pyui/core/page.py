"""Page PyUI : conteneur plein écran associé à une route."""

import tkinter as tk

from pyui.core.component import Component
from pyui.theme.theme import Theme


class Page(Component):
    """Une page de l'application (Niveau 4, Phase 8).

    Hooks : on_show() / on_hide() appelés lors de la navigation.

    Exemple :
        class DashboardPage(Page):
            def render(self):
                Label(self, text="Tableau de bord", size="2xl", weight="bold")
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, app=None, route=None, title=None, padding=16):
        self.app = app
        self.route = route
        self.page_title = title
        self.padding = padding
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=padding, pady=padding)

    def on_show(self):
        """Appelé quand la page devient active (après navigation)."""

    def on_hide(self):
        """Appelé quand la page cesse d'être active (avant destruction)."""

    def _apply_theme(self):
        self._apply_bg("background")
