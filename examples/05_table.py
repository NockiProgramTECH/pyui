"""Table de données PyUI : tri, recherche, pagination, export (Niveau 6)."""

from pyui import App, Page, Label, DataTable, Card, Dialog


USERS = [
    {"name": "Awa Koné", "email": "awa@example.com", "phone": "+225 07 01 02 03", "ville": "Abidjan"},
    {"name": "Jean Kouassi", "email": "jean@example.com", "phone": "+225 05 04 03 02", "ville": "Abidjan"},
    {"name": "Fatou Diallo", "email": "fatou@example.com", "phone": "+221 77 123 45 67", "ville": "Dakar"},
    {"name": "Marc N'Guessan", "email": "marc@example.com", "phone": "+225 01 99 88 77", "ville": "Bouaké"},
    {"name": "Léa Traoré", "email": "lea@example.com", "phone": "+225 07 55 44 33", "ville": "Yamoussoukro"},
    {"name": "Oumar Sy", "email": "oumar@example.com", "phone": "+221 70 111 22 33", "ville": "Dakar"},
    {"name": "Nadia Bamba", "email": "nadia@example.com", "phone": "+225 05 66 77 88", "ville": "San-Pédro"},
    {"name": "Paul Yao", "email": "paul@example.com", "phone": "+225 07 22 11 00", "ville": "Abidjan"},
    {"name": "Seydou Camara", "email": "seydou@example.com", "phone": "+223 76 12 34 56", "ville": "Bamako"},
    {"name": "Rita Gnahoré", "email": "rita@example.com", "phone": "+225 01 44 55 66", "ville": "Daloa"},
    {"name": "Idrissa Sow", "email": "idrissa@example.com", "phone": "+221 78 90 12 34", "ville": "Saint-Louis"},
    {"name": "Claire Mensah", "email": "claire@example.com", "phone": "+228 90 87 65 43", "ville": "Lomé"},
]


class UsersPage(Page):
    def render(self):
        Label(self, text="Clients", size="2xl", weight="bold")

        card = Card(self, title="Liste des clients", subtitle=f"{len(USERS)} enregistrements")

        def on_select(rows):
            if rows:
                self.status.set_subtitle(f"Sélectionné : {rows[0]['name']} ({rows[0]['email']})")

        def on_double_click(row):
            self.status.set_subtitle(f"Double-clic sur {row['name']}")

        def on_delete(row):
            def confirm():
                self.table.remove_row(lambda r: r["name"] == row["name"])
                self.status.set_subtitle(f"{row['name']} supprimé")
            Dialog.confirm(f"Supprimer {row['name']} ?", on_confirm=confirm)

        self.table = DataTable(
            card,
            columns=[
                ("name", "Nom"),
                ("email", "Email"),
                ("phone", "Téléphone"),
                ("ville", "Ville"),
            ],
            data=USERS,
            searchable=True,
            paginate=True,
            page_size=5,
            exportable=True,
            on_select=on_select,
            on_double_click=on_double_click,
            on_edit=lambda row: self.status.set_subtitle(f"Modifier : {row['name']}"),
            on_delete=on_delete,
        )
        self.table.pack(fill="both", expand=True, pady=(8, 0))

        self.status = Card(self, title="Statut", subtitle="Cliquez sur une ligne")
        self.status.pack(fill="x", pady=(12, 0))


def main():
    app = App(title="PyUI — DataTable", size=(900, 620))
    app.add_route("/", UsersPage)
    app.navigate("/")
    app.run()


if __name__ == "__main__":
    main()