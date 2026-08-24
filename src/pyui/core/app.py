"""Application PyUI : fenêtre, thème, état, événements, routes et historique."""

import tkinter as tk

from pyui.core.events import EventBus
from pyui.core.router import Router
from pyui.core.state import State
from pyui.layouts.container import Container
from pyui.theme.theme import Theme


class App:
    """Application principale.

    Exemple :
        app = App(title="Mon application", size=(1000, 700))
        app.add_route("/", DashboardPage, title="Dashboard")
        app.add_route("/clients", ClientsPage, title="Clients")
        app.navigate("/")
        app.back()  # navigation précédente
        app.run()
    """

    def __init__(self, title="PyUI", size=(1000, 700), min_size=(800, 600),
                 theme="light"):
        self._root = tk.Tk()
        self._root.title(title)
        if size:
            self._root.geometry(f"{size[0]}x{size[1]}")
        if min_size:
            self._root.minsize(*min_size)

        self.title = title
        self.theme = Theme
        self.events = EventBus()
        self.state = State()
        self.router = Router()

        self._page = None
        self._content = None
        self._root_children = []
        self._before_navigate = []
        self._after_navigate = []

        self._root.configure(bg=Theme.get("background"))
        self._root.protocol("WM_DELETE_WINDOW", self.close)
        Theme.set_mode(theme)

    # ------------------------------------------------------------------
    @property
    def tk(self):
        """La fenêtre racine Tk."""
        return self._root

    @property
    def page(self):
        """La page actuellement affichée (ou None)."""
        return self._page

    @property
    def current_path(self):
        """Le chemin de la page actuelle (ou None)."""
        return self.router.current_path

    def run(self):
        """Lance la boucle d'événements (bloquant)."""
        self._root.mainloop()

    def close(self):
        """Ferme la fenêtre et l'application (détruit d'abord les composants)."""
        for child in list(self._root_children):
            child.destroy()
        self._root_children.clear()
        self._root.quit()
        self._root.destroy()

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------
    def add_route(self, path, page_cls, name=None, title=None):
        """Enregistre une page pour un chemin.

        Ex : app.add_route("/clients", ClientsPage, title="Clients")
        """
        self.router.add(path, page_cls, name=name, title=title)
        return self

    def routes(self):
        """Renvoie les routes enregistrées (dict chemin -> Route)."""
        return self.router.routes

    def before_navigate(self, callback):
        """Enregistre un hook appelé avec (path) avant chaque navigation."""
        self._before_navigate.append(callback)
        return self

    def after_navigate(self, callback):
        """Enregistre un hook appelé avec (path, page) après chaque navigation."""
        self._after_navigate.append(callback)
        return self

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def navigate(self, path, record=True):
        """Affiche la page associée au chemin et émet l'événement "navigate"."""
        if path not in self.router.routes:
            raise KeyError(f"Route inconnue : {path!r}")
        for callback in self._before_navigate:
            callback(path)
        self._render_page(path)
        if record:
            self.router.push(path)
        self.events.emit("navigate", path=path)
        for callback in self._after_navigate:
            callback(path, self._page)
        return self._page

    def back(self):
        """Revient à la page précédente (historique)."""
        path = self.router.back()
        if path is not None:
            self.navigate(path, record=False)
        return path

    def forward(self):
        """Avance à la page suivante (après un retour)."""
        path = self.router.forward()
        if path is not None:
            self.navigate(path, record=False)
        return path

    @property
    def can_back(self):
        return self.router.can_back

    @property
    def can_forward(self):
        return self.router.can_forward

    def set_content(self, container):
        """Définit le conteneur dans lequel les pages sont affichées."""
        self._content = container
        return self

    def _render_page(self, path):
        if self._content is None:
            self._content = Container(self, padding=0, fill=True, expand=True)
        if self._page is not None:
            self._page.on_hide()
            self._page.destroy()
        page_cls = self.router.routes[path].page
        self._page = page_cls(self._content, app=self, route=path)
        self._page.on_show()
        return self._page

    def _add_child(self, child):
        self._root_children.append(child)

    def __repr__(self):
        return f"<App title={self.title!r}>"