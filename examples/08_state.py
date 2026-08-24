"""État réactif : compteur lié via State + bind_state (Phase 10)."""

from pyui import App, Page, Button, Label, Row, Column, State, Theme, Separator


# ---------------------------------------------------------------------------
# État global
# ---------------------------------------------------------------------------
state = State({
    "count": 0,
    "theme": "light",
    "user": "Inconnu",
})


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
class CounterPage(Page):
    def render(self):
        Label(self, text="Compteur réactif", size="2xl", weight="bold")

        # Le label affiche la valeur de state["count"] automatiquement
        counter = Label(self, text="0", size="3xl", weight="bold")
        counter.bind_state(state, "count", "text")

        row = Row(self, spacing=8)
        row.add(Button, text="−", icon="minus", variant="secondary",
                command=lambda: state.set("count", state.get("count") - 1))
        row.add(Button, text="+", icon="plus",
                command=lambda: state.set("count", state.get("count") + 1))

        Separator(self, orientation="horizontal").pack(fill="x", pady=12)

        # État utilisateur
        Label(self, text="Utilisateur", size="xl", weight="bold")
        user_label = Label(self, text="", size="lg", color="muted")
        user_label.bind_state(state, "user", "text")

        # Bouton de simulation de changement utilisateur
        def set_user():
            state.set("user", "Awa Koné")
            state.set("count", state.get("count") + 1)

        Button(self, text="Connecter utilisateur", variant="secondary", command=set_user)


class SettingsPage(Page):
    def render(self):
        Label(self, text="Paramètres", size="2xl", weight="bold")

        # Snapshots : état en temps réel
        Label(self, text="État actuel :", size="sm", color="muted")
        self.state_label = Label(self, text="", size="sm")
        self.state_label.bind_state(state, "count", lambda c, v: setattr(self.state_label, "text", str(state.snapshot())))

        Button(self, text="Réinitialiser le compteur", variant="ghost",
               command=lambda: state.set("count", 0))
        Button(self, text="Réinitialiser tout", variant="ghost",
               command=state.reset)
        Button(self, text="Ajouter 10", variant="secondary",
               command=lambda: state.set("count", state.get("count") + 10))


# ---------------------------------------------------------------------------
# Thème via l'état
# ---------------------------------------------------------------------------
def on_theme(key, value, old):
    Theme.dark() if value == "dark" else Theme.light()


state.subscribe("theme", on_theme)


def toggle_theme():
    state.set("theme", "dark" if Theme.mode() == "light" else "light")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
def main():
    app = App(title="PyUI — État réactif", size=(700, 500))

    from pyui import Sidebar, Navbar, Footer, Container, Column

    Sidebar(app, title="State", items=[
        {"key": "counter", "text": "Compteur", "icon": "plus", "route": "/"},
        {"key": "settings", "text": "Paramètres", "icon": "settings", "route": "/settings"},
    ], app=app)

    right = Column(app, spacing=0)
    navbar = Navbar(right, title="Compteur", actions=[
        {"text": "Thème", "icon": "settings", "variant": "ghost", "command": toggle_theme},
    ])
    content = Container(right, padding=12, fill=True, expand=True)
    app.set_content(content)
    Footer(right, text="© 2026 PyUI — State management")

    app.add_route("/", CounterPage, title="Compteur")
    app.add_route("/settings", SettingsPage, title="Paramètres")
    app.navigate("/")
    app.run()


if __name__ == "__main__":
    main()