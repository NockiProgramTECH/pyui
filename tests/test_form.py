"""Tests des validateurs de formulaires."""

import pytest

from pyui.forms.validators import (
    ValidationError, required, min_length, max_length,
    is_email, is_number, match_regex,
)


def test_required():
    required("x")
    with pytest.raises(ValidationError):
        required("")
    with pytest.raises(ValidationError):
        required(None)


def test_min_length():
    min_length("abc", 3)
    with pytest.raises(ValidationError):
        min_length("ab", 3)


def test_max_length():
    max_length("ab", 3)
    with pytest.raises(ValidationError):
        max_length("abcd", 3)


def test_is_email():
    is_email("user@example.com")
    with pytest.raises(ValidationError):
        is_email("pas-un-email")
    is_email("")  # vide accepté sauf si required


def test_is_number():
    is_number("42")
    is_number("3.14")
    with pytest.raises(ValidationError):
        is_number("abc")


def test_match_regex():
    match_regex("ABC", r"^[A-Z]+$")
    with pytest.raises(ValidationError):
        match_regex("abc", r"^[A-Z]+$")


# ---------------------------------------------------------------------------
# Champs
# ---------------------------------------------------------------------------
def test_textfield_validation():
    from pyui.forms.fields import TextField

    field = TextField("name", label="Nom", required=True, min_length=3, max_length=50)
    field.value = "ab"
    assert field.validate() is False
    assert field.error is not None

    field.value = "Jean"
    assert field.validate() is True
    assert field.error is None

    field.value = ""
    assert field.validate() is False  # obligatoire


def test_email_validation():
    from pyui.forms.fields import EmailField

    field = EmailField("email", label="Email", required=True)
    field.value = "mauvais"
    assert field.validate() is False
    field.value = "user@example.com"
    assert field.validate() is True


def test_number_validation_and_conversion():
    from pyui.forms.fields import NumberField

    field = NumberField("age", label="Âge", min=18, max=99)
    field.value = "abc"
    assert field.validate() is False

    field.value = "25"
    assert field.validate() is True
    assert field.get() == 25

    field.value = "5"
    assert field.validate() is False  # < min


def test_custom_validator():
    from pyui.forms.fields import TextField
    from pyui.forms.validators import ValidationError

    def even(value):
        if int(value) % 2 != 0:
            raise ValidationError("Doit être pair")

    field = TextField("n", validator=even)
    field.value = "3"
    assert field.validate() is False
    field.value = "4"
    assert field.validate() is True


# ---------------------------------------------------------------------------
# Formulaire
# ---------------------------------------------------------------------------
def test_form_values_and_set_values(app):
    from pyui import Form, TextField, EmailField

    form = Form(
        app,
        fields=[
            TextField("name", label="Nom"),
            EmailField("email", label="Email"),
        ],
    )
    form.set_values({"name": "Awa", "email": "awa@example.com"})
    values = form.values()
    assert values["name"] == "Awa"
    assert values["email"] == "awa@example.com"


def test_form_validate_required(app):
    from pyui import Form, TextField

    form = Form(app, fields=[TextField("name", label="Nom", required=True)])
    assert form.validate() is False
    name = form.get_field("name")
    assert name.error is not None

    name.set("Jean")
    assert form.validate() is True
    assert name.error is None


def test_form_submit(app):
    from pyui import Form, TextField, EmailField

    submitted = []

    form = Form(
        app,
        fields=[
            TextField("name", label="Nom", required=True),
            EmailField("email", label="Email", required=True),
        ],
        on_submit=lambda values: submitted.append(values),
    )
    assert form.submit() is False  # invalide -> pas de soumission
    assert submitted == []

    form.set_values({"name": "Jean", "email": "jean@example.com"})
    assert form.submit() is True
    assert submitted == [{"name": "Jean", "email": "jean@example.com"}]


def test_form_clear(app):
    from pyui import Form, TextField, CheckboxField

    form = Form(
        app,
        fields=[
            TextField("name", label="Nom"),
            CheckboxField("terms", text="Accepter"),
        ],
    )
    form.set_values({"name": "Jean", "terms": True})
    form.clear()
    assert form.values()["name"] == ""
    assert form.values()["terms"] is False


def test_form_error_display(app):
    from pyui import Form, TextField

    form = Form(app, fields=[TextField("name", label="Nom", required=True)])
    form.validate()
    field = form.get_field("name")
    assert field._error_label is not None
    assert field.error is not None
    assert field._error_label._visible is True  # erreur affichée