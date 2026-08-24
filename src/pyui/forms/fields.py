"""Champs de formulaire PyUI (Niveau 5).

Chaque champ est un objet de configuration + validation. La construction du
widget de saisie a lieu à l'ajout au Formulaire (Form).

Exemple :
    TextField("name", label="Nom", required=True, min_length=3, max_length=50)
    EmailField("email", label="Email")
    PasswordField("password", label="Mot de passe")
"""

import re
from datetime import datetime

from pyui.forms.validators import (
    ValidationError, required, min_length, max_length,
    is_email, is_number, match_regex,
)


class FormField:
    """Classe de base d'un champ de formulaire."""

    def __init__(self, name, label=None, required=False, min_length=None,
                 max_length=None, pattern=None, validator=None, help_text=None,
                 initial=None):
        self.name = name
        self.label = label or name.capitalize()
        self.required = required
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
        self.validator = validator
        self.help_text = help_text
        self.value = initial
        self.error = None
        self._widget = None
        self._error_label = None

    # ------------------------------------------------------------------
    # Construction du widget
    # ------------------------------------------------------------------
    def build(self, parent):
        """Crée le widget de saisie du champ dans `parent`."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Valeur
    # ------------------------------------------------------------------
    def get(self):
        if self._widget is not None:
            return self._widget.get()
        return self.value

    def set(self, value):
        self.value = value
        if self._widget is not None:
            self._widget.set(value)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate(self):
        """Valide la valeur saisie. Renvoie True/False et remplit self.error."""
        value = self.get()
        self.error = None
        try:
            if self.required:
                required(value, "Champ obligatoire")
            if value is None or str(value).strip() == "":
                return True
            if self.min_length is not None:
                min_length(value, self.min_length,
                           f"Minimum {self.min_length} caractères")
            if self.max_length is not None:
                max_length(value, self.max_length,
                           f"Maximum {self.max_length} caractères")
            if self.pattern:
                match_regex(value, self.pattern, "Format invalide")
            self._check(value)
        except ValidationError as exc:
            self.error = str(exc)
            return False
        if self.validator is not None:
            try:
                self.validator(value)
            except ValidationError as exc:
                self.error = str(exc)
                return False
        return True

    def _check(self, value):
        """Hook de validation spécifique au type de champ."""


class TextField(FormField):
    """Champ de texte libre."""

    def __init__(self, name, label=None, required=False, min_length=None,
                 max_length=None, pattern=None, validator=None, help_text=None,
                 initial=None, placeholder=None):
        self.placeholder = placeholder
        super().__init__(name, label=label, required=required,
                         min_length=min_length, max_length=max_length,
                         pattern=pattern, validator=validator,
                         help_text=help_text, initial=initial)

    def build(self, parent):
        from pyui.widgets.input import Input
        return Input(parent,
                     value="" if self.value is None else str(self.value),
                     placeholder=self.placeholder)


class PasswordField(TextField):
    """Champ de mot de passe (saisie masquée)."""

    def build(self, parent):
        from pyui.widgets.input import Input
        return Input(parent,
                     value="" if self.value is None else str(self.value),
                     placeholder=self.placeholder,
                     show="\u2022")


class NumberField(FormField):
    """Champ numérique avec min/max."""

    def __init__(self, name, label=None, required=False, min_length=None,
                 max_length=None, pattern=None, validator=None, help_text=None,
                 initial=None, min=None, max=None):
        super().__init__(name, label=label, required=required,
                         min_length=min_length, max_length=max_length,
                         pattern=pattern, validator=validator,
                         help_text=help_text, initial=initial)
        self.min = min
        self.max = max

    def build(self, parent):
        from pyui.widgets.input import Input
        return Input(parent,
                     value="" if self.value is None else str(self.value))

    def get(self):
        raw = super().get()
        if raw is None or str(raw).strip() == "":
            return None
        try:
            return int(raw)
        except (TypeError, ValueError):
            try:
                return float(raw)
            except (TypeError, ValueError):
                return raw

    def _check(self, value):
        is_number(value, "Valeur numérique requise")
        number = float(value)
        if self.min is not None and number < self.min:
            raise ValidationError(f"Minimum : {self.min}")
        if self.max is not None and number > self.max:
            raise ValidationError(f"Maximum : {self.max}")


class EmailField(TextField):
    """Champ email validé par format."""

    def _check(self, value):
        is_email(value, "Adresse email invalide")


class SelectField(FormField):
    """Champ à choix unique (liste déroulante)."""

    def __init__(self, name, label=None, required=False, min_length=None,
                 max_length=None, pattern=None, validator=None, help_text=None,
                 initial=None, options=None):
        super().__init__(name, label=label, required=required,
                         min_length=min_length, max_length=max_length,
                         pattern=pattern, validator=validator,
                         help_text=help_text, initial=initial)
        self.options = list(options or [])

    def build(self, parent):
        from pyui.widgets.select import Select
        return Select(parent, options=self.options, value=self.value)


class CheckboxField(FormField):
    """Champ booléen (case à cocher)."""

    def __init__(self, name, label=None, required=False, min_length=None,
                 max_length=None, pattern=None, validator=None, help_text=None,
                 initial=None, text=None):
        super().__init__(name, label=label, required=required,
                         min_length=min_length, max_length=max_length,
                         pattern=pattern, validator=validator,
                         help_text=help_text, initial=initial)
        self.text = text or label

    def build(self, parent):
        from pyui.widgets.checkbox import CheckBox
        return CheckBox(parent, text=self.text, checked=bool(self.value))

    def get(self):
        if self._widget is not None:
            return self._widget.is_checked
        return bool(self.value)

    def set(self, value):
        self.value = bool(value)
        if self._widget is not None:
            self._widget.is_checked = bool(value)

    def validate(self):
        if self.required and not self.get():
            self.error = "Cette case doit être cochée"
            return False
        self.error = None
        return True


class DateField(TextField):
    """Champ date au format AAAA-MM-JJ."""

    def build(self, parent):
        from pyui.widgets.input import Input
        return Input(parent,
                     value="" if self.value is None else str(self.value),
                     placeholder="AAAA-MM-JJ")

    def _check(self, value):
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(value)):
            raise ValidationError("Format attendu : AAAA-MM-JJ")
        try:
            datetime.strptime(str(value), "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Date invalide")


class FileField(FormField):
    """Champ fichier : saisie + bouton Parcourir."""

    def __init__(self, name, label=None, required=False, min_length=None,
                 max_length=None, pattern=None, validator=None, help_text=None,
                 initial=None, filetypes=None):
        super().__init__(name, label=label, required=required,
                         min_length=min_length, max_length=max_length,
                         pattern=pattern, validator=validator,
                         help_text=help_text, initial=initial)
        self.filetypes = list(filetypes) if filetypes else [("Tous les fichiers", "*.*")]
        self._entry = None

    def build(self, parent):
        from pyui.layouts.row import Row
        from pyui.widgets.button import Button
        from pyui.widgets.input import Input

        row = Row(parent, spacing=4)
        self._entry = Input(row, value="" if self.value is None else str(self.value))
        Button(row, text="Parcourir", variant="secondary", command=self._browse)
        return row

    def _browse(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=self.filetypes)
        if path:
            self.set(path)

    def get(self):
        if self._entry is not None:
            return self._entry.get()
        return self.value

    def set(self, value):
        self.value = value
        if self._entry is not None:
            self._entry.set(value)