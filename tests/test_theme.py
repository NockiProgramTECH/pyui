"""Tests du thème (Design System, dark mode)."""

import pytest


def test_default_mode(app):
    from pyui import Theme
    assert Theme.mode() == "light"
    assert Theme.get("primary") == "#2563EB"


def test_switch_dark_light(app):
    from pyui import Theme
    Theme.dark()
    assert Theme.mode() == "dark"
    assert Theme.get("background") == "#0F172A"
    Theme.light()
    assert Theme.mode() == "light"
    assert Theme.get("background") == "#F8FAFC"


def test_set_mode_invalid(app):
    from pyui import Theme
    with pytest.raises(ValueError):
        Theme.set_mode("pink")


def test_configure_tokens(app):
    from pyui import Theme
    Theme.configure(primary="#123456")
    assert Theme.get("primary") == "#123456"


def test_font(app):
    from pyui import Theme
    font = Theme.font("base", "bold")
    assert font[0] == "Segoe UI"
    assert font[2] == "bold"


def test_components_react_to_theme(app):
    from pyui import Theme, Button

    button = Button(app, text="B", variant="primary")
    bg_light = button.tk.cget("bg")
    Theme.dark()
    bg_dark = button.tk.cget("bg")
    assert bg_light != bg_dark