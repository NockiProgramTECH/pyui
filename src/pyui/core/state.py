"""Gestion d'état réactif PyUI (Niveau 13, Phase 10).

Les composants peuvent s'abonner à l'état et se mettre à jour automatiquement.

Exemple :
    state = State({"user": None, "theme": "light", "sidebar_open": True})
    state.set("theme", "dark")

    # Liaison d'une clé d'état à un composant :
    label.bind_state(state, "user", "text")

    # Abonnement sur une clé :
    state.subscribe("theme", lambda key, value, old: Theme.dark() if value == "dark" else Theme.light())
"""

import weakref

_MISSING = object()


class State:
    """État observable : get/set, abonnement par clé ou global, liaison composants."""

    def __init__(self, initial=None):
        self._data = dict(initial or {})
        self._initial = dict(self._data)
        self._listeners = {}   # key -> [callback(key, value, old)]
        self._all = []         # [callback(key, value, old)] pour toutes les clés

    # ------------------------------------------------------------------
    # Lecture / écriture
    # ------------------------------------------------------------------
    def get(self, key, default=None):
        """Renvoie la valeur de la clé (ou `default`)."""
        return self._data.get(key, default)

    def has(self, key):
        """Vrai si la clé existe dans l'état."""
        return key in self._data

    def set(self, key, value):
        """Définit une valeur et notifie les abonnés."""
        old = self._data.get(key, _MISSING)
        if old == value:
            return
        self._data[key] = value
        self.notify(key, value, old)

    def update(self, **data):
        """Met à jour plusieurs clés à la fois.

        Exemple : state.update(user="Awa", theme="dark")
        """
        for key, value in data.items():
            self.set(key, value)

    def replace(self, data):
        """Remplace tout l'état et notifie les clés modifiées."""
        snapshot = dict(self._data)
        self._data = dict(data or {})
        for key, value in self._data.items():
            if snapshot.get(key, _MISSING) != value:
                self.notify(key, value, snapshot.get(key, _MISSING))

    def reset(self):
        """Rétablit l'état initial."""
        self.replace(self._initial)

    def snapshot(self):
        """Renvoie une copie de l'état complet."""
        return dict(self._data)

    # ------------------------------------------------------------------
    # Abonnement
    # ------------------------------------------------------------------
    def subscribe(self, key, callback=None):
        """Abonne un callback aux changements d'état.

        - state.subscribe("theme", cb)  : cb(key, value, old) pour la clé "theme"
        - state.subscribe(cb)           : cb(key, value, old) pour toutes les clés

        Renvoie une fonction de désabonnement.
        """
        if callback is None:
            callback = key
            key = None

        if key is None:
            self._all.append(callback)
            target = self._all
        else:
            self._listeners.setdefault(key, []).append(callback)
            target = self._listeners[key]

        def unsubscribe():
            if callback in target:
                target.remove(callback)

        return unsubscribe

    def unsubscribe(self, key, callback):
        """Désabonne un callback (raccourci)."""
        if key is None:
            if callback in self._all:
                self._all.remove(callback)
        else:
            handlers = self._listeners.get(key)
            if handlers and callback in handlers:
                handlers.remove(callback)

    def notify(self, key, value, old=_MISSING):
        """Notifie les abonnés d'un changement de clé."""
        for callback in list(self._all):
            callback(key, value, old)
        for callback in list(self._listeners.get(key, ())):
            callback(key, value, old)

    # ------------------------------------------------------------------
    # Liaison aux composants
    # ------------------------------------------------------------------
    def bind(self, component, key, target=None):
        """Lie une clé d'état à un composant.

        `target` : nom d'attribut (str) ou callable(component, value).
        Si `target` est None, on utilise le nom de la clé comme attribut.

        Exemple :
            state.bind(label, "count", "text")
            state.bind(button, "enabled", lambda b, v: b.enable() if v else b.disable())

        Renvoie la fonction de désabonnement.
        """
        if target is None:
            target = key
        ref = weakref.ref(component)

        def binder(_key, value, old):
            comp = ref()
            if comp is None or getattr(comp, "_destroyed", True):
                return
            if callable(target):
                target(comp, value)
            else:
                setattr(comp, target, value)

        return self.subscribe(key, binder)

    def __repr__(self):
        return f"<State {self._data!r}>"