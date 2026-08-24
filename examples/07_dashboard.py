"""Dashboard PyUI : stats, graphique, activités, timeline, onglets, badges (Phase 9)."""

from pyui import (
    App, Page, Sidebar, Navbar, Footer, Container, Column,
    Dashboard, Toast, Theme, Tabs, Label, Badge, Alert, Accordion, Card,
)


class DashboardPage(Page):
    def render(self):
        Label(self, text="Dashboard", size="2xl", weight="bold")

        Dashboard(
            self,
            stats=[
                {"title": "Clients", "value": "1 245", "icon": "users", "delta": "+12%"},
                {"title": "Ventes", "value": "86", "icon": "chart", "delta": "+8%"},
                {"title": "Stock", "value": "312", "icon": "box", "delta": "-3%"},
                {"title": "CA", "value": "2 450 000 FCFA", "icon": "money", "delta": "+21%"},
            ],
            chart={
                "kind": "bar",
                "title": "Ventes par mois",
                "data": {
                    "labels": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
                    "values": [120, 180, 140, 220, 260, 310],
                },
            },
            activity=[
                {"icon": "user", "text": "Nouveau client : Awa", "time": "il y a 5 min"},
                {"icon": "cart", "text": "Vente #1024", "time": "il y a 20 min"},
                {"icon": "box", "text": "Stock faible : article 12", "time": "il y a 1 h"},
            ],
            actions=[
                {"text": "Nouveau client", "icon": "plus",
                 "command": lambda: Toast.info("Ajouter un client")},
                {"text": "Exporter", "icon": "download",
                 "command": lambda: Toast.success("Export terminé")},
            ],
            timeline=[
                {"title": "Commande livrée", "time": "14:30",
                 "text": "Commande #1024 livrée à Abidjan"},
                {"title": "Client créé", "time": "13:05",
                 "text": "Awa K. a été ajoutée à la base"},
            ],
        )


class ComposantsPage(Page):
    def render(self):
        Label(self, text="Composants avancés", size="2xl", weight="bold")

        row = Column(self, spacing=8)

        alerts = Column(row, spacing=6)
        Alert(alerts, message="Client enregistré avec succès", variant="success", dismissible=True)
        Alert(alerts, message="Stock faible pour 3 articles", variant="warning", dismissible=True)
        Alert(alerts, message="Erreur de connexion au serveur", variant="danger")

        badges = Column(row, spacing=6)
        from pyui import Row as HRow
        hr = HRow(badges, spacing=8)
        hr.add(Badge, text="Actif", variant="success")
        hr.add(Badge, text="12", variant="primary")
        hr.add(Badge, text="Brouillon", variant="default")
        hr.add(Badge, text="En retard", variant="danger")

        Card(row, title="Onglets")
        Tabs(row, tabs=[
            {"text": "Clients", "content": lambda p: Label(p, text="Liste des clients")},
            {"text": "Ventes", "content": lambda p: Label(p, text="Ventes du jour")},
            {"text": "Rapports", "content": lambda p: Label(p, text="Rapports mensuels")},
        ])

        Card(row, title="Accordéon")
        Accordion(row, sections=[
            {"title": "Général", "content": lambda p: Label(p, text="Informations générales")},
            {"title": "Avancé", "content": lambda p: Label(p, text="Options avancées")},
        ])


def main():
    app = App(title="PyUI — Dashboard", size=(1200, 760))

    Sidebar(app, title="PyUI", items=[
        {"key": "dash", "text": "Dashboard", "icon": "home", "route": "/"},
        {"key": "composants", "text": "Composants", "icon": "settings", "route": "/composants"},
    ], app=app)

    right = Column(app, spacing=0)
    navbar = None

    def toggle_theme():
        if Theme.mode() == "light":
            Theme.dark()
            navbar.set_title("Mode sombre")
        else:
            Theme.light()
            navbar.set_title("Mode clair")

    navbar = Navbar(right, title="Dashboard", actions=[
        {"icon": "arrow-left", "variant": "ghost", "command": app.back},
        {"icon": "arrow-right", "variant": "ghost", "command": app.forward},
        {"icon": "bell", "variant": "ghost"},
        {"text": "Thème", "icon": "settings", "variant": "ghost", "command": toggle_theme},
    ])

    content = Container(right, padding=12, fill=True, expand=True)
    app.set_content(content)
    Footer(right, text="© 2026 PyUI — Dashboard")

    app.add_route("/", DashboardPage, title="Dashboard")
    app.add_route("/composants", ComposantsPage, title="Composants")
    app.navigate("/")
    app.run()


if __name__ == "__main__":
    main()