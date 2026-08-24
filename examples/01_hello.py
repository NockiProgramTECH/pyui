"""Application de démonstration PyUI (Niveau 0-1)."""

from pyui import (
    App, Button, Label, Column, Row, Card, Input, CheckBox, Separator, Theme,
)


def main():
    app = App(title="PyUI — Démo", size=(800, 600))

    col = Column(app, spacing=8)
    col.pack(fill="both", expand=True, padx=24, pady=24)

    Label(col, text="Bienvenue dans PyUI", size="2xl", weight="bold")
    Label(col, text="Votre framework GUI Python", color="muted", size="lg")

    Separator(col, orientation="horizontal").pack(fill="x", pady=8)

    card = Card(col, title="Démo", subtitle="Composants de base")
    Input(card, placeholder="Saisissez du texte")
    CheckBox(card, text="Activer l'option")

    actions = Row(card, spacing=8)
    actions.add(Button, text="Valider", variant="primary")
    actions.add(Button, text="Annuler", variant="ghost")

    def toggle_theme():
        if Theme.mode() == "light":
            Theme.dark()
            theme_btn.text = "Passer en mode clair"
        else:
            Theme.light()
            theme_btn.text = "Passer en mode sombre"

    theme_btn = Button(col, text="Passer en mode sombre", variant="secondary",
                       command=toggle_theme)

    app.run()


if __name__ == "__main__":
    main()