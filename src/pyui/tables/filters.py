"""Filtrage et recherche pour DataTable."""


class Filter:
    """Filtre sur une ou plusieurs colonnes."""

    def __init__(self, column=None, operator="contains", value=None):
        self.column = column
        self.operator = operator
        self.value = value
