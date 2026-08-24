"""Moteur de formulaires PyUI (Niveau 5).

Exemple :
    form = Form(
        parent,
        fields=[
            TextField("name", label="Nom", required=True),
            EmailField("email", label="Email"),
            PasswordField("password", label="Mot de passe"),
        ],
        buttons=[
            {"text": "Enregistrer", "variant": "primary", "type": "submit"},
            {"text": "Annuler", "variant": "ghost", "type": "reset"},
        ],
        on_submit=create_user,
    )
"""

import tkinter as tk

from pyui.core.component import Component
from pyui.layouts.row import Row
from pyui.widgets.button import Button
from pyui.widgets.frame import Frame
from pyui.widgets.label import Label
from pyui.forms.fields import CheckboxField, FormField


class Form(Component):
    """Formulaire avec rendu, validation et soumission."""

    _tk_class = tk.Frame

    def __init__(self, parent=None, fields=None, on_submit=None, buttons=None,
                 spacing=10):
        self.field_specs = list(fields or [])
        self.on_submit = on_submit
        self.buttons = list(buttons or [])
        self.spacing = spacing
        self._fields = {}
        super().__init__(parent)

    def render(self):
        for field in self.field_specs:
            row = Frame(self, padding=0)
            row.pack(fill="x", pady=self.spacing // 2)

            label_text = field.label + (" *" if field.required else "")
            Label(row, text=label_text, size="sm", weight="bold").pack(anchor="w", pady=(0, 2))

            widget = field.build(row)
            widget.pack(fill="x")

            error = Label(row, text="", color="danger", size="sm")
            error.pack(anchor="w")
            error.hide()

            field._widget = widget
            field._error_label = error
            self._fields[field.name] = field

        if self.buttons:
            actions = Row(self, spacing=8)
            actions.pack(fill="x", pady=(self.spacing // 2, 0))
            for spec in self.buttons:
                command = spec.get("command")
                if spec.get("type") == "submit":
                    command = self.submit
                elif spec.get("type") == "reset":
                    command = self.clear
                actions.add(Button,
                            text=spec.get("text", ""),
                            variant=spec.get("variant", "primary"),
                            icon=spec.get("icon"),
                            command=command)

    # ------------------------------------------------------------------
    # Valeurs
    # ------------------------------------------------------------------
    def values(self):
        """Renvoie les valeurs saisies sous forme de dict {name: valeur}."""
        return {field.name: field.get() for field in self.field_specs}

    def set_values(self, data):
        """Pré-remplit les champs depuis un dict."""
        for field in self.field_specs:
            if field.name in data:
                field.set(data[field.name])
        return self

    def get_field(self, name):
        """Renvoie le champ par son nom (ou None)."""
        return self._fields.get(name)

    @property
    def fields(self):
        return self.field_specs

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate(self):
        """Valide tous les champs et affiche les erreurs. Renvoie True si OK."""
        ok = True
        for field in self.field_specs:
            valid = field.validate()
            self._show_error(field)
            ok = ok and valid
        return ok

    def _show_error(self, field):
        if field._error_label is None:
            return
        if field.error:
            field._error_label.text = field.error
            field._error_label.show()
        else:
            field._error_label.hide()

    # ------------------------------------------------------------------
    # Soumission
    # ------------------------------------------------------------------
    def submit(self):
        """Valide puis appelle on_submit(values) si le formulaire est valide."""
        if not self.validate():
            return False
        if self.on_submit is not None:
            self.on_submit(self.values())
        return True

    def clear(self):
        """Réinitialise les champs et efface les erreurs."""
        for field in self.field_specs:
            if isinstance(field, CheckboxField):
                field.set(False)
            else:
                field.set("")
            field.error = None
            self._show_error(field)
        return self