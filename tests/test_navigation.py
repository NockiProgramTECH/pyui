"""Tests de navigation (routes, historique, hooks)."""

import pytest


def _make_app(app):
    from pyui import Page, Label

    class HomePage(Page):
        def render(self):
            Label(self, text="Accueil")

    class ClientsPage(Page):
        def render(self):
            Label(self, text="Clients")

    class ProductsPage(Page):
        def render(self):
            Label(self, text="Produits")

    app.add_route("/", HomePage, title="Accueil")
    app.add_route("/clients", ClientsPage, title="Clients")
    app.add_route("/products", ProductsPage, title="Produits")
    return {"home": HomePage, "clients": ClientsPage, "products": ProductsPage}


def test_app_routes_and_navigation(app):
    pages = _make_app(app)
    app.navigate("/")
    assert isinstance(app.page, pages["home"])
    assert app.current_path == "/"

    app.navigate("/clients")
    assert isinstance(app.page, pages["clients"])


def test_app_navigate_unknown_route(app):
    from pyui import Page

    app.add_route("/", Page)
    with pytest.raises(KeyError):
        app.navigate("/inconnue")


def test_app_page_is_destroyed_on_navigation(app):
    from pyui import Page, Label

    destroyed = []

    class FirstPage(Page):
        def render(self):
            Label(self, text="1")

        def destroy(self):
            destroyed.append(True)
            super().destroy()

    class SecondPage(Page):
        def render(self):
            Label(self, text="2")

    app.add_route("/1", FirstPage)
    app.add_route("/2", SecondPage)

    app.navigate("/1")
    first = app.page
    app.navigate("/2")

    assert first._destroyed is True
    assert destroyed == [True]


def test_app_history_back_forward(app):
    pages = _make_app(app)
    app.navigate("/")
    app.navigate("/clients")
    app.navigate("/products")

    assert app.current_path == "/products"
    assert app.can_back is True

    app.back()
    assert app.current_path == "/clients"
    assert isinstance(app.page, pages["clients"])

    app.back()
    assert app.current_path == "/"
    assert app.can_back is False
    app.back()  # au début de l'historique
    assert app.current_path == "/"

    app.forward()
    assert app.current_path == "/clients"
    app.forward()
    assert app.current_path == "/products"
    assert app.can_forward is False


def test_app_route_titles(app):
    _make_app(app)
    app.navigate("/clients")
    assert app.router.current_route.title == "Clients"
    assert app.router.get("/").title == "Accueil"


def test_app_before_after_navigate_hooks(app):
    _make_app(app)
    events = []

    app.before_navigate(lambda path: events.append(("before", path)))
    app.after_navigate(lambda path, page: events.append(("after", path)))

    app.navigate("/clients")
    assert ("before", "/clients") in events
    assert ("after", "/clients") in events


def test_app_page_show_hide_hooks(app):
    from pyui import Page, Label

    calls = []

    class PageA(Page):
        def on_show(self):
            calls.append("A:show")

        def on_hide(self):
            calls.append("A:hide")

        def render(self):
            Label(self, text="A")

    class PageB(Page):
        def render(self):
            Label(self, text="B")

    app.add_route("/a", PageA)
    app.add_route("/b", PageB)

    app.navigate("/a")
    app.navigate("/b")
    app.navigate("/a")

    assert calls == ["A:show", "A:hide", "A:show"]


def test_router_standalone():
    from pyui import Router

    router = Router()
    router.add("/a", object, title="A")
    router.add("/b", object, title="B")
    router.push("/a")
    router.push("/b")

    assert router.current_path == "/b"
    assert router.can_back is True
    assert router.back() == "/a"
    assert router.forward() == "/b"
    assert router.current_route.title == "B"
    assert "/a" in router.routes