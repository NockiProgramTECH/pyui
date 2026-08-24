"""Tests du modèle de placement (pack, grid, place) — Phase 10 amélioration."""

import pytest

from pyui import Pack, Place, GridPlacement


def test_pack_stores_placement(app):
    from pyui import Button

    btn = Button(app, text="OK")
    btn.pack(side="left", fill="y", padx=8, pady=(4, 4))
    assert isinstance(btn.placement, Pack)
    assert btn.placement.side == "left"
    assert btn.placement.fill == "y"
    assert btn.placement.padx == 8


def test_pack_show_hide_restores(app):
    from pyui import Button, Column

    col = Column(app, spacing=4)
    btn = Button(col, text="OK")
    btn.hide()
    assert btn._visible is False
    btn.show()
    assert btn._visible is True
    assert isinstance(btn.placement, Pack)


def test_grid_placement(app):
    from pyui import Button

    btn = Button(app, text="A")
    btn.grid(row=1, column=2, sticky="nsew", columnspan=2)
    assert isinstance(btn.placement, GridPlacement)
    assert btn.placement.row == 1
    assert btn.placement.column == 2
    assert btn.placement.columnspan == 2


def test_place_placement(app):
    from pyui import Button

    btn = Button(app, text="B")
    btn.place(x=10, y=20, width=100, height=30)
    assert isinstance(btn.placement, Place)
    assert btn.placement.x == 10
    assert btn.placement.width == 100


def test_layout_accepts_model(app):
    from pyui import Button

    btn = Button(app, text="C")
    btn.layout(Pack(side="right", fill="both", expand=True, padx=12))
    assert isinstance(btn.placement, Pack)
    assert btn.placement.side == "right"
    assert btn.placement.expand is True


def test_layout_replaces_previous(app):
    from pyui import Button

    btn = Button(app, text="D")
    btn.pack(side="top")
    btn.layout(Place(x=5, y=5))
    assert isinstance(btn.placement, Place)


def test_pack_invalid_side(app):
    from pyui import Button

    btn = Button(app, text="E")
    with pytest.raises(ValueError):
        btn.pack(side="diagonale")


def test_pack_invalid_fill(app):
    from pyui import Button

    btn = Button(app, text="F")
    with pytest.raises(ValueError):
        btn.pack(fill="bothx")


def test_pack_invalid_padding(app):
    from pyui import Button

    btn = Button(app, text="G")
    with pytest.raises(ValueError):
        btn.pack(padx="10")


def test_pack_expand_must_be_bool(app):
    from pyui import Button

    btn = Button(app, text="H")
    with pytest.raises(ValueError):
        btn.pack(expand="oui")


def test_grid_invalid_sticky(app):
    from pyui import Button

    btn = Button(app, text="I")
    with pytest.raises(ValueError):
        btn.grid(row=0, column=0, sticky="xyz")


def test_place_invalid_rel(app):
    from pyui import Button

    btn = Button(app, text="J")
    with pytest.raises(ValueError):
        btn.place(relx=1.5)


def test_placement_to_dict(app):
    from pyui import Button

    btn = Button(app, text="K")
    btn.pack(side="top", fill="x", padx=(4, 8))
    data = btn.placement.to_dict()
    assert data["side"] == "top"
    assert data["padx"] == (4, 8)


def test_model_classes_validation():
    with pytest.raises(ValueError):
        Pack(side="gauche")
    with pytest.raises(ValueError):
        GridPlacement(sticky="nq")
    with pytest.raises(ValueError):
        Place(relx=2)