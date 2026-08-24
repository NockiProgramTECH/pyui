"""Tests de la Sidebar, Navbar et icônes (Phase 4)."""


def test_sidebar_creation(app):
    from pyui import Sidebar

    sidebar = Sidebar(
        app,
        title="Menu",
        items=[
            {"key": "a", "text": "Item A", "icon": "home"},
            {"key": "b", "text": "Item B"},
        ],
    )
    assert len(sidebar._rows) == 2
    assert sidebar.active is None


def test_sidebar_active_and_command(app):
    from pyui import Sidebar

    clicked = []

    sidebar = Sidebar(
        app,
        items=[
            {"key": "a", "text": "A", "command": lambda: clicked.append("a")},
            {"key": "b", "text": "B", "command": lambda: clicked.append("b")},
        ],
    )
    row_a = sidebar._rows[0]
    row_a["button"].invoke()
    assert sidebar.active == "a"
    assert clicked == ["a"]

    sidebar.set_active("b")
    assert sidebar.active == "b"


def test_sidebar_route_navigation(app):
    from pyui import Sidebar, Page, Label

    class Home(Page):
        def render(self):
            Label(self, text="Accueil")

    class Clients(Page):
        def render(self):
            Label(self, text="Clients")

    app.add_route("/", Home)
    app.add_route("/clients", Clients)

    sidebar = Sidebar(
        app,
        items=[
            {"key": "home", "text": "Accueil", "route": "/"},
            {"key": "clients", "text": "Clients", "route": "/clients"},
        ],
        app=app,
    )
    sidebar._rows[1]["button"].invoke()
    assert isinstance(app.page, Clients)
    assert sidebar.active == "clients"


def test_sidebar_submenu_toggle(app):
    from pyui import Sidebar

    sidebar = Sidebar(
        app,
        items=[
            {"text": "Parent", "children": [
                {"key": "c1", "text": "Enfant 1", "route": "/x"},
            ]},
        ],
    )
    parent_row = sidebar._rows[0]
    assert parent_row["expanded"] is False
    parent_row["button"].invoke()
    assert parent_row["expanded"] is True
    parent_row["button"].invoke()
    assert parent_row["expanded"] is False


def test_sidebar_collapse(app):
    from pyui import Sidebar

    sidebar = Sidebar(app, items=[{"text": "A"}])
    sidebar.collapse()
    assert sidebar.collapsed is True
    sidebar.expand()
    assert sidebar.collapsed is False


def test_sidebar_theme_update(app):
    from pyui import Sidebar, Theme

    sidebar = Sidebar(app, items=[{"key": "a", "text": "A"}])
    sidebar.set_active("a")
    bg_light = sidebar._rows[0]["button"].cget("bg")
    Theme.dark()
    bg_dark = sidebar._rows[0]["button"].cget("bg")
    assert bg_light != bg_dark


def test_navbar_creation_and_actions(app):
    from pyui import Navbar

    clicked = []

    nav = Navbar(app, title="Titre", actions=[
        {"text": "Action", "variant": "ghost", "command": lambda: clicked.append(1)},
    ])
    assert nav.nav_title == "Titre"
    assert len(nav._action_buttons) == 1
    nav._action_buttons[0].tk.invoke()
    assert clicked == [1]
    nav.set_title("Autre")
    assert nav.nav_title == "Autre"


def test_footer_creation(app):
    from pyui import Footer

    footer = Footer(app, text="© 2026 PyUI")
    assert footer.footer_text == "© 2026 PyUI"


def test_icon_manager():
    from pyui import IconManager, GLYPHS

    assert IconManager.glyph("home") != ""
    assert IconManager.glyph("home") == GLYPHS["home"]
    assert IconManager.glyph("inconnu") == ""


def test_button_with_icon(app):
    from pyui import Button, IconManager

    button = Button(app, text="Clients", icon="users")
    assert IconManager.glyph("users") in button.tk.cget("text")