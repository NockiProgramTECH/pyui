"""Application de gestion de clients — exemple complet (docs/tutorial.md).

Fonctionnalités : Sidebar + Navbar + navigation, formulaire avec validation,
DataTable avec recherche/pagination/suppression, toasts, dark mode.
"""

from pyui import (
    App, Page, Sidebar, Navbar, Footer, Container, Column,
    Label, Card, Form, TextField, EmailField, DataTable,
    Theme, Toast, Dialog,
)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
class DashboardPage(Page):
    def render(self):
        Label(self, text="Dashboard", size="2xl", weight="bold")
        total = len(self.app.clients)
        Card(self, title="Clients", subtitle=f"{total} enregistrés")
        Card(self, title="Actions", subtitle="Utilisez le menu latéral")


class ClientsListPage(Page):
    def render(self):
        Label(self, text="Liste des clients", size="2xl", weight="bold")
        Card(self, title="Clients", subtitle=f"{len(self.app.clients)} enregistrements")

        self.table = DataTable(
            self,
            columns=[
                ("nom", "Nom"),
                ("email", "Email"),
                ("telephone", "Téléphone"),
            ],
            data=self.app.clients,
            searchable=True,
            paginate=True,
            page_size=5,
            on_delete=self.supprimer,
        )
        self.table.pack(fill="both", expand=True, pady=8)

    def supprimer(self, row):
        def do_delete():
            self.app.clients = [c for c in self.app.clients if c["email"] != row["email"]]
            self.table.set_data(self.app.clients)
            Toast.info(f"{row['nom']} supprimé")

        Dialog.confirm(f"Supprimer {row['nom']} ?", on_confirm=do_delete)


class AjoutClientPage(Page):
    def render(self):
        Label(self, text="Nouveau client", size="2xl", weight="bold")
        Card(self, title="Informations")
        self.form = Form(
            self,
            fields=[
                TextField("nom", label="Nom", required=True, min_length=2),
                EmailField("email", label="Email", required=True),
                TextField("telephone", label="Téléphone", required=True),
            ],
            buttons=[
                {"text": "Enregistrer", "icon": "save", "variant": "primary", "type": "submit"},
                {"text": "Annuler", "variant": "ghost", "command": self.annuler},
            ],
            on_submit=self.ajouter,
        )

    def ajouter(self, values):
        self.app.clients.append(values)
        Toast.success(f"Client {values['nom']} ajouté")
        self.app.navigate("/clients")

    def annuler(self):
        if self.app.back() is None:
            self.app.navigate("/")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
def main():
    app = App(title="Gestion de clients — PyUI", size=(1000, 680))
    app.clients = []

    sidebar = Sidebar(app, title="Gestion", items=[
        {"key": "dashboard", "text": "Dashboard", "icon": "home", "route": "/"},
        {"key": "clients", "text": "Clients", "icon": "users", "route": "/clients"},
        {"key": "ajout", "text": "Nouveau client", "icon": "plus", "route": "/ajout"},
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
    Footer(right, text="© 2026 PyUI — Application de gestion")

    app.add_route("/", DashboardPage)
    app.add_route("/clients", ClientsListPage)
    app.add_route("/ajout", AjoutClientPage)

    app.navigate("/")
    app.run()


if __name__ == "__main__":
    main()