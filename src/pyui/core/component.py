"""Composant de base de PyUI.

Tous les composants héritent de :class:`Component` et respectent le cycle de vie :

    create -> render -> update -> destroy

Le composant possède aussi une API commune (spécification Niveau 1) :

    component.show()
    component.hide()
    component.destroy()
    component.configure()
    component.pack()
    component.grid()
    component.place()
"""

import tkinter as tk
import weakref

from pyui.core.placement import Pack, Grid, Place
from pyui.theme.theme import Theme


class Component:
    """Classe de base de tous les composants PyUI."""

    _tk_class = None
    bg_token = "background"

    def __init__(self, parent=None, **kwargs):
        self.parent = parent
        self.children = []
        self._tk = None
        self._destroyed = False
        self._visible = True
        self._placement = None
        self._theme_unsubscribe = None
        self._state_unsubs = []
        self.create(**kwargs)
        if parent is not None:
            add_child = getattr(parent, "_add_child", None)
            if add_child is not None:
                add_child(self)
        self._subscribe_theme()

    # ------------------------------------------------------------------
    # Cycle de vie : create -> render -> update -> destroy
    # ------------------------------------------------------------------
    def create(self, **kwargs):
        """Crée le widget Tkinter sous-jacent puis appelle render()."""
        if self._tk_class is not None:
            self._tk = self._tk_class(self._parent_tk(), **self._widget_kwargs(**kwargs))
            self._apply_theme()
        self.render()

    def render(self):
        """Hook de rendu : construit le contenu interne du composant."""

    def update(self, **kwargs):
        """Met à jour des propriétés du widget Tkinter."""
        if self._tk is not None:
            self._tk.configure(**kwargs)
        return self

    def configure(self, **kwargs):
        """Alis de update() : configure le composant."""
        return self.update(**kwargs)

    def destroy(self):
        """Détruit le composant, ses enfants et se désabonne du thème/état."""
        if self._destroyed:
            return
        for child in list(self.children):
            child.destroy()
        self.children.clear()
        if self._theme_unsubscribe is not None:
            self._theme_unsubscribe()
            self._theme_unsubscribe = None
        for unsubscribe in list(self._state_unsubs):
            unsubscribe()
        self._state_unsubs.clear()
        if self._tk is not None:
            self._tk.destroy()
            self._tk = None
        self._destroyed = True

    # ------------------------------------------------------------------
    # Accès au widget Tkinter
    # ------------------------------------------------------------------
    @property
    def tk(self):
        """Le widget Tkinter sous-jacent (ou celui de l'App pour le parent)."""
        return self._tk

    def _parent_tk(self):
        if self.parent is None:
            return None
        if isinstance(self.parent, tk.Misc):
            return self.parent
        return getattr(self.parent, "tk", None)

    def _widget_kwargs(self, **kwargs):
        """Transforme les arguments PyUI en arguments Tkinter."""
        return {k: v for k, v in kwargs.items() if v is not None}

    # ------------------------------------------------------------------
    # Thème réactif
    # ------------------------------------------------------------------
    def _apply_theme(self):
        """Hook appelé à la création et à chaque changement de thème."""

    def _subscribe_theme(self):
        ref = weakref.ref(self)

        def handler():
            obj = ref()
            if obj is None or obj._destroyed or obj._tk is None:
                return
            try:
                obj._apply_theme()
            except tk.TclError:
                # Le widget a été détruit avec la fenêtre racine : on se désabonne.
                obj._tk = None
                obj._destroyed = True
                if obj._theme_unsubscribe is not None:
                    obj._theme_unsubscribe()
                    obj._theme_unsubscribe = None

        self._theme_unsubscribe = Theme.subscribe(handler)

    def _apply_bg(self, token=None):
        """Applique la couleur de fond du token (ou bg_token) sur un Frame."""
        if self._tk is not None:
            self._tk.configure(bg=Theme.get(token or self.bg_token))

    # ------------------------------------------------------------------
    # Liaison à l'état
    # ------------------------------------------------------------------
    def bind_state(self, state, key, target=None):
        """Lie une clé d'état à une propriété du composant.

        Le composant est automatiquement mis à jour quand la clé change,
        et se désabonne à la destruction.

        Exemple :
            label.bind_state(state, "count", "text")
            button.bind_state(state, "enabled", lambda b, v: b.enable() if v else b.disable())
        """
        unsub = state.bind(self, key, target)
        if unsub is not None:
            self._state_unsubs.append(unsub)
        return self

    # ------------------------------------------------------------------
    # Visibilité
    # ------------------------------------------------------------------
    def show(self):
        """Affiche le composant (restaure son placement)."""
        self._visible = True
        if self._tk is not None and self._placement is not None:
            self._placement.apply(self._tk)
        return self

    def hide(self):
        """Masque le composant (le placement est conservé)."""
        self._visible = False
        if self._tk is not None and self._placement is not None:
            self._placement.remove(self._tk)
        return self

    # ------------------------------------------------------------------
    # Placement (pack / grid / place)
    # ------------------------------------------------------------------
    @property
    def placement(self):
        """Le modèle de placement appliqué (Pack, Grid ou Place)."""
        return self._placement

    def layout(self, placement):
        """Applique un modèle de placement (Pack, Grid ou Place).

        Remplace l'ancien placement si le composant était déjà positionné.
        """
        if self._tk is not None and self._placement is not None:
            self._placement.remove(self._tk)
        self._placement = placement
        if self._tk is not None and self._visible:
            placement.apply(self._tk)
        return self

    def pack(self, side="top", fill=None, expand=False, anchor=None,
             padx=0, pady=0, ipadx=0, ipady=0):
        """Place le composant par empilement (pack).

        side   : "top", "bottom", "left" ou "right"
        fill   : None, "x", "y" ou "both"
        expand : occuper l'espace libre restant (booléen)
        anchor : position dans la zone allouée ("n", "s", "e", "w", "center"...)
        padx   : espacement horizontal externe (px)
        pady   : espacement vertical externe (px)
        ipadx  : espacement horizontal interne (px)
        ipady  : espacement vertical interne (px)
        """
        return self.layout(Pack(side=side, fill=fill, expand=expand, anchor=anchor,
                                padx=padx, pady=pady, ipadx=ipadx, ipady=ipady))

    def grid(self, row=None, column=None, rowspan=1, columnspan=1,
             sticky=None, padx=0, pady=0, ipadx=0, ipady=0):
        """Place le composant dans une grille (grid).

        row        : ligne (0, 1, 2...)
        column     : colonne (0, 1, 2...)
        rowspan    : nombre de lignes fusionnées
        columnspan : nombre de colonnes fusionnées
        sticky     : étirement ("n", "s", "e", "w" combinables, ex: "nsew")
        padx       : espacement horizontal externe (px)
        pady       : espacement vertical externe (px)
        ipadx      : espacement horizontal interne (px)
        ipady      : espacement vertical interne (px)
        """
        return self.layout(Grid(row=row, column=column, rowspan=rowspan,
                                columnspan=columnspan, sticky=sticky,
                                padx=padx, pady=pady, ipadx=ipadx, ipady=ipady))

    def place(self, x=None, y=None, relx=None, rely=None, anchor=None,
              width=None, height=None, relwidth=None, relheight=None):
        """Place le composant en position absolue (place).

        x, y        : position en pixels depuis le coin supérieur gauche
        relx, rely  : position relative (0.0 à 1.0 de la taille du parent)
        anchor      : point d'ancrage ("nw", "n", "center"...)
        width       : largeur en pixels
        height      : hauteur en pixels
        relwidth    : largeur relative (0.0 à 1.0)
        relheight   : hauteur relative (0.0 à 1.0)
        """
        return self.layout(Place(x=x, y=y, relx=relx, rely=rely, anchor=anchor,
                                 width=width, height=height,
                                 relwidth=relwidth, relheight=relheight))

    # ------------------------------------------------------------------
    # Événements
    # ------------------------------------------------------------------
    def bind(self, sequence, callback=None, add=None):
        if self._tk is not None:
            return self._tk.bind(sequence, callback, add)
        return ""

    def unbind(self, sequence, funcid=None):
        if self._tk is not None:
            self._tk.unbind(sequence, funcid)

    def focus(self):
        if self._tk is not None:
            self._tk.focus_set()
        return self

    # ------------------------------------------------------------------
    # Enfants
    # ------------------------------------------------------------------
    def _add_child(self, child):
        self.children.append(child)

    def _remove_child(self, child):
        if child in self.children:
            self.children.remove(child)

    def __repr__(self):
        return f"<{type(self).__name__} tk={self._tk!r}>"
