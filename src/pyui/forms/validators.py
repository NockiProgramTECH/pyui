"""Validateurs de champs (Niveau 5)."""


class ValidationError(Exception):
    """Erreur de validation d'un champ."""


def required(value, message="Champ obligatoire"):
    if value is None or str(value).strip() == "":
        raise ValidationError(message)


def min_length(value, length, message=None):
    if value is not None and len(str(value)) < length:
        raise ValidationError(message or f"Minimum {length} caractères")


def max_length(value, length, message=None):
    if value is not None and len(str(value)) > length:
        raise ValidationError(message or f"Maximum {length} caractères")


def is_email(value, message="Email invalide"):
    import re
    if value is not None and value.strip() and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(value)):
        raise ValidationError(message)


def is_number(value, message="Valeur numérique requise"):
    try:
        float(value)
    except (TypeError, ValueError):
        raise ValidationError(message)


def match_regex(value, pattern, message="Format invalide"):
    import re
    if value is not None and value.strip() and not re.match(pattern, str(value)):
        raise ValidationError(message)


def custom(validator, value):
    """Appelle une fonction de validation personnalisée (lève ValidationError)."""
    validator(value)
