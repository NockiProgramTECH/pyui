"""Application type : Sidebar + Navbar + pages + thème (Phase 4)."""

from pyui import (
    App, Page, Sidebar, Navbar, Footer, Container, Column, Row, Grid,
    StatCard, Button, Label, Card, Theme, Separator, IconManager,
)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
class DashboardPage(Page):
    def render(self):
        Label(self, text="Dashboard", size="2xl", weight="bold")
        Separator(self, orientation="horizontal").pack(fill="x", pady=8)

        grid = Grid(self, columns=4, spacing=8)
        grid.add(StatCard, title="Clients", value="1 245", icon="users", delta="+12%")
        grid.add(StatCard, title="Ventes", value="86", icon="chart", delta="+8%")
        grid.add(StatCard, title="Stock", value="312", icon="box", delta="-3%")
        grid.add(StatCard, title="Chiffre d'affaires", value="2 450 000 FCFA", icon="money", delta="+21%")

        col = Column(self, spacing=8)
        Card(col, title="Activité récente", subtitle="Aucune activité pour le moment")


class ClientsPage(Page):
    def render(self):
        Label(self, text="Clients", size="2xl", weight="bold")
        Separator(self, orientation="horizontal").pack(fill="x", pady=8)
        Card(self, title="Liste des clients", subtitle="Module en construction")


class VentesNouvellePage(Page):
    def render(self):
        Label(self, text="Nouvelle vente", size="2xl", weight="bold")
        Separator(self, orientation="horizontal").pack(fill="x", pady=8)
        Card(self, title="Formulaire de vente", subtitle="Fonctionnalité à venir")


class VentesHistoriquePage(Page):
    def render(self):
        Label(self, text="Historique des ventes", size="2xl", weight="bold")
        Separator(self, orientation="horizontal").pack(fill="x", pady=8)
        Card(self, title="Historique", subtitle="Fonctionnalité à venir")


class StockPage(Page):
    def render(self):
        Label(self, text="Stock", size="2xl", weight="bold")
        Separator(self, orientation="horizontal").pack(fill="x", pady=8)
        Card(self, title="Gestion des stocks", subtitle="Fonctionnalité à venir")


class SettingsPage(Page):
    def render(self):
        Label(self, text="Paramètres", size="2xl", weight="bold")
        Separator(self, orientation="horizontal").pack(fill="x", pady=8)
        Card(self, title="Configuration", subtitle="Préférences utilisateur")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
def main():
    app = App(title="Gestion commerciale — PyUI", size=(1200, 760))

    # Sidebar
    sidebar = Sidebar(
        app,
        title="PyUI",
        logo="\u25A6",
        items=[
            {"key": "dashboard", "text": "Dashboard",   "icon": "home",     "route": "/"},
            {"key": "clients",   "text": "Clients",      "icon": "users",    "route": "/clients"},
            {"text": "Ventes",   "icon": "chart", "children": [
                {"key": "ventes_nouvelle",  "text": "Nouvelle vente",  "route": "/ventes/nouvelle"},
                {"key": "ventes_historique", "text": "Historique",      "route": "/ventes/historique"},
            ]},
            {"key": "stock",     "text": "Stock",         "icon": "box",      "route": "/stock"},
            {"key": "settings",  "text": "Paramètres",    "icon": "settings", "route": "/settings"},
        ],
        app=app,
    )

    # Partie droite : Navbar + contenu + Footer
    right = Column(app, spacing=0, align="stretch")

    def toggle_theme():
        if Theme.mode() == "light":
            Theme.dark()
            nav.set_title("Mode sombre")
        else:
            Theme.light()
            nav.set_title("Mode clair")

    nav = Navbar(right, title="Dashboard", actions=[
        {"icon": "bell", "variant": "ghost"},
        {"text": "Thème", "icon": "settings", "variant": "ghost", "command": toggle_theme},
    ])

    content = Container(right, padding=12, fill=True, expand=True)
    app.set_content(content)

    Footer(right, text="\u00A9 2026 PyUI — Framework GUI Python")

    # Routes
    app.add_route("/", DashboardPage)
    app.add_route("/clients", ClientsPage)
    app.add_route("/ventes/nouvelle", VentesNouvellePage)
    app.add_route("/ventes/historique", VentesHistoriquePage)
    app.add_route("/stock", StockPage)
    app.add_route("/settings", SettingsPage)

    app.navigate("/")
    app.run()


if __name__ == "__main__":
    main()