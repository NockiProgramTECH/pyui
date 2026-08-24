"""Tests du composant de base (cycle de vie et API commune)."""

import pytest


def test_component_lifecycle(app):
    from pyui import Component

    lifecycle = []

    class Probe(Component):
        def create(self, **kwargs):
            lifecycle.append("create")
            super().create(**kwargs)

        def render(self):
            lifecycle.append("render")

        def destroy(self):
            lifecycle.append("destroy")
            super().destroy()

    probe = Probe(app)
    probe.destroy()

    assert lifecycle == ["create", "render", "destroy"]
    assert probe._destroyed is True


def test_common_api(app):
    from pyui import Label

    label = Label(app, text="Hello")
    label.configure(text="Bonjour")
    label.update(text="Salut")
    label.hide()
    label.show()
    label.destroy()

    assert label._destroyed is True


def test_show_hide(app):
    from pyui import Label, Column

    col = Column(app, spacing=4)
    col.pack(fill="both", expand=True)

    label = Label(col, text="Visible")
    label.hide()
    assert label._visible is False
    label.show()
    assert label._visible is True


def test_children_destroyed_with_parent(app):
    from pyui import Column, Label

    col = Column(app, spacing=4)
    child = Label(col, text="enfant")
    col.destroy()

    assert child._destroyed is True