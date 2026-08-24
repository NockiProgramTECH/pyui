"""Formulaire PyUI avec validation (Niveau 5)."""

from pyui import (
    App, Page, Card, Column, Form, TextField, EmailField, PasswordField,
    NumberField, SelectField, CheckboxField, DateField, FileField, Label,
)


class ContactPage(Page):
    def render(self):
        Label(self, text="Créer un compte", size="2xl", weight="bold")

        card = Card(self, title="Informations", subtitle="Les champs * sont obligatoires")

        def on_submit(values):
            self.result_card.set_subtitle("Données valides — " + str(values))

        self.form = Form(
            card,
            fields=[
                TextField("name", label="Nom complet", required=True, min_length=3, max_length=50),
                EmailField("email", label="Email", required=True),
                PasswordField("password", label="Mot de passe", required=True, min_length=6),
                NumberField("age", label="Âge", min=18, max=99),
                SelectField("pays", label="Pays", options=["Côte d'Ivoire", "Sénégal", "France", "Canada"]),
                DateField("birthday", label="Date de naissance"),
                CheckboxField("terms", label="", text="J'accepte les conditions", required=True),
                FileField("avatar", label="Photo de profil"),
            ],
            buttons=[
                {"text": "Enregistrer", "icon": "save", "variant": "primary", "type": "submit"},
                {"text": "Réinitialiser", "variant": "ghost", "type": "reset"},
            ],
            on_submit=on_submit,
        )

        self.form.set_values({"name": "Awa", "pays": "Côte d'Ivoire"})

        self.result_card = Card(self, title="Résultat", subtitle="Aucune soumission")
        self.result_card.pack(fill="x", pady=(12, 0))


def main():
    app = App(title="PyUI — Formulaires", size=(720, 820))
    app.add_route("/", ContactPage)
    app.navigate("/")
    app.run()


if __name__ == "__main__":
    main()