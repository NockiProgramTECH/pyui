"""Tests de l'application."""


def test_app_creation(app):
    assert app.title == "Test"
    assert app.tk is not None