"""Routeur PyUI : applications multi-pages avec historique (Niveau 8)."""


class Route:
    """Une route : chemin, classe de page, nom et titre optionnel."""

    def __init__(self, path, page_cls, name=None, title=None):
        self.path = path
        self.page = page_cls
        self.name = name or path
        self.title = title or name or path


class Router:
    """Gère les routes, la page courante et l'historique de navigation.

    Exemple :
        router = Router()
        router.add("/", HomePage)
        router.add("/clients", ClientsPage, name="clients", title="Clients")
        router.push("/clients")
        router.current_path  # → "/clients"
        router.back()        # → "/"
        router.forward()     # → "/clients"
    """

    def __init__(self):
        self._routes = {}
        self._history = []
        self._index = -1

    def add(self, path, page_cls, name=None, title=None):
        """Enregistre une route avec la classe de page.

        name : identifiant optionnel (str), title : titre affichable (str).
        """
        self._routes[path] = Route(path, page_cls, name=name, title=title)
        return self

    def remove(self, path):
        """Supprime une route."""
        self._routes.pop(path, None)

    def get(self, path):
        """Renvoie l'objet Route pour un chemin (ou None)."""
        return self._routes.get(path)

    @property
    def routes(self):
        """Renvoie un dict {chemin: Route} de toutes les routes."""
        return dict(self._routes)

    @property
    def current_path(self):
        """Chemin de la page actuelle (ou None)."""
        if 0 <= self._index < len(self._history):
            return self._history[self._index]
        return None

    @property
    def current_route(self):
        """Renvoie l'objet Route de la page actuelle (ou None)."""
        path = self.current_path
        return self._routes.get(path) if path else None

    @property
    def can_back(self):
        """Vrai si on peut revenir à la page précédente."""
        return self._index > 0

    @property
    def can_forward(self):
        """Vrai si on peut avancer après un retour."""
        return self._index < len(self._history) - 1

    def push(self, path):
        """Enregistre une navigation dans l'historique."""
        self._history = self._history[: self._index + 1]
        self._history.append(path)
        self._index = len(self._history) - 1

    def back(self):
        """Revient à la page précédente. Renvoie le chemin ou None."""
        if self.can_back:
            self._index -= 1
            return self.current_path
        return None

    def forward(self):
        """Avance à la page suivante. Renvoie le chemin ou None."""
        if self.can_forward:
            self._index += 1
            return self.current_path
        return None

    def reset(self):
        """Vide l'historique."""
        self._history.clear()
        self._index = -1