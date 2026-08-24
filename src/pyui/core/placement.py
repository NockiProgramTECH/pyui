"""Modèle de placement des widgets PyUI (grid, pack, place).

Les méthodes Component.pack(), Component.grid() et Component.place() utilisent
ces modèles en interne. On peut aussi les instancier directement pour composer
un placement réutilisable :

    from pyui import Pack, Place, GridPlacement

    bouton.layout(Pack(side="left", fill="y", padx=8))
    bouton.layout(Place(x=10, y=20, width=100))
    bouton.layout(GridPlacement(row=0, column=1, sticky="nsew"))
"""


class Placement:
    """Classe de base d'un placement de widget."""

    manager = "pack"

    def apply(self, widget):
        """Applique le placement au widget Tkinter."""
        raise NotImplementedError

    def remove(self, widget):
        """Retire le widget de son conteneur (sans le détruire)."""
        if self.manager == "pack":
            widget.pack_forget()
        elif self.manager == "grid":
            widget.grid_remove()
        elif self.manager == "place":
            widget.place_forget()

    def to_dict(self):
        """Renvoie les paramètres du placement sous forme de dict."""
        return dict(self.__dict__)

    def __repr__(self):
        args = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{type(self).__name__}({args})"


_SIDES = ("top", "bottom", "left", "right")
_FILLS = (None, "x", "y", "both")
_ANCHORS = (None, "n", "ne", "e", "se", "s", "sw", "w", "nw", "center")


def _check(value, choices, name):
    if value not in choices:
        raise ValueError(
            f"{name} invalide : {value!r}. Valeurs possibles : {choices}")


def _check_int(value, name, minimum=0):
    if not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} doit être un entier >= {minimum}")


def _check_padding(value, name):
    """padx/pady acceptent un entier ou un tuple (a, b)."""
    if isinstance(value, int):
        if value < 0:
            raise ValueError(f"{name} doit être un entier >= 0")
        return
    if (isinstance(value, (tuple, list)) and len(value) == 2
            and all(isinstance(v, int) and v >= 0 for v in value)):
        return
    raise ValueError(
        f"{name} doit être un entier >= 0 ou un tuple (a, b)")


def _check_bool(value, name):
    if not isinstance(value, bool):
        raise ValueError(f"{name} doit être un booléen (True/False)")


class Pack(Placement):
    """Placement par empilement (pack).

    Paramètres :
        side     : côté d'ancrage ("top", "bottom", "left", "right")
        fill     : étirement (None, "x", "y", "both")
        expand   : occuper l'espace libre restant (bool)
        anchor   : position dans la zone allouée ("n", "s", "e", "w", "center"...)
        padx     : espacement horizontal externe (px)
        pady     : espacement vertical externe (px)
        ipadx    : espacement horizontal interne (px)
        ipady    : espacement vertical interne (px)
    """

    manager = "pack"

    def __init__(self, side="top", fill=None, expand=False, anchor=None,
                 padx=0, pady=0, ipadx=0, ipady=0):
        _check(side, _SIDES, "side")
        _check(fill, _FILLS, "fill")
        _check(anchor, _ANCHORS, "anchor")
        _check_bool(expand, "expand")
        _check_padding(padx, "padx")
        _check_padding(pady, "pady")
        _check_padding(ipadx, "ipadx")
        _check_padding(ipady, "ipady")
        self.side = side
        self.fill = fill
        self.expand = expand
        self.anchor = anchor
        self.padx = padx
        self.pady = pady
        self.ipadx = ipadx
        self.ipady = ipady

    def apply(self, widget):
        widget.pack(side=self.side, fill=self.fill, expand=self.expand,
                    anchor=self.anchor, padx=self.padx, pady=self.pady,
                    ipadx=self.ipadx, ipady=self.ipady)


class Grid(Placement):
    """Placement par grille (grid).

    Paramètres :
        row        : ligne (0, 1, 2...)
        column     : colonne (0, 1, 2...)
        rowspan    : nombre de lignes fusionnées
        columnspan : nombre de colonnes fusionnées
        sticky     : étirement (combinaison de "n", "s", "e", "w")
        padx       : espacement horizontal externe (px)
        pady       : espacement vertical externe (px)
        ipadx      : espacement horizontal interne (px)
        ipady      : espacement vertical interne (px)
    """

    manager = "grid"

    def __init__(self, row=None, column=None, rowspan=1, columnspan=1,
                 sticky=None, padx=0, pady=0, ipadx=0, ipady=0):
        if row is not None:
            _check_int(row, "row")
        if column is not None:
            _check_int(column, "column")
        _check_int(rowspan, "rowspan", 1)
        _check_int(columnspan, "columnspan", 1)
        _check_padding(padx, "padx")
        _check_padding(pady, "pady")
        _check_padding(ipadx, "ipadx")
        _check_padding(ipady, "ipady")
        if sticky is not None:
            if not isinstance(sticky, str) or not set(sticky) <= set("nsew"):
                raise ValueError("sticky doit être une combinaison de 'n','s','e','w'")
        self.row = row
        self.column = column
        self.rowspan = rowspan
        self.columnspan = columnspan
        self.sticky = sticky
        self.padx = padx
        self.pady = pady
        self.ipadx = ipadx
        self.ipady = ipady

    def apply(self, widget):
        widget.grid(row=self.row, column=self.column, rowspan=self.rowspan,
                    columnspan=self.columnspan, sticky=self.sticky,
                    padx=self.padx, pady=self.pady,
                    ipadx=self.ipadx, ipady=self.ipady)


class Place(Placement):
    """Placement absolu (place).

    Paramètres :
        x, y        : position en pixels depuis le coin supérieur gauche
        relx, rely  : position relative (0.0 à 1.0 de la taille du parent)
        anchor      : point d'ancrage ("nw", "n", "center"...)
        width       : largeur en pixels
        height      : hauteur en pixels
        relwidth    : largeur relative (0.0 à 1.0)
        relheight   : hauteur relative (0.0 à 1.0)
    """

    manager = "place"

    def __init__(self, x=None, y=None, relx=None, rely=None, anchor=None,
                 width=None, height=None, relwidth=None, relheight=None):
        for name, value in (("x", x), ("y", y), ("width", width), ("height", height)):
            if value is not None:
                _check_int(value, name, -10**6)
        for name, value in (("relx", relx), ("rely", rely),
                            ("relwidth", relwidth), ("relheight", relheight)):
            if value is not None:
                if not isinstance(value, (int, float)) or not 0.0 <= value <= 1.0:
                    raise ValueError(f"{name} doit être un nombre entre 0.0 et 1.0")
        _check(anchor, _ANCHORS, "anchor")
        self.x = x
        self.y = y
        self.relx = relx
        self.rely = rely
        self.anchor = anchor
        self.width = width
        self.height = height
        self.relwidth = relwidth
        self.relheight = relheight

    def apply(self, widget):
        widget.place(x=self.x, y=self.y, relx=self.relx, rely=self.rely,
                     anchor=self.anchor, width=self.width, height=self.height,
                     relwidth=self.relwidth, relheight=self.relheight)