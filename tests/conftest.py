"""Configuration pytest : une seule App Tk partagée (Tk ne supporte pas
la recréation de racines dans le même processus sous Windows)."""

import pytest


@pytest.fixture(scope="session")
def app():
    from pyui import App
    instance = App(title="Test", size=(800, 600))
    yield instance
    instance.close()


@pytest.fixture(autouse=True)
def _clean_ui(app):
    """Nettoye l'interface entre chaque test et remet le thème en clair."""
    yield
    for child in list(app._root_children):
        child.destroy()
    app._root_children.clear()
    app._page = None
    app._content = None
    app.router.reset()
    from pyui import Theme
    if Theme.mode() != "light":
        Theme.light()
