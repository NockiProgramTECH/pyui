# Formulaires

## `Form`

Générateur de formulaires avec validation automatique et soumission.

```python
form = Form(
    parent,
    fields=[
        TextField("name", label="Nom", required=True, min_length=3),
        EmailField("email", label="Email", required=True),
        PasswordField("password", label="Mot de passe", required=True, min_length=6),
        NumberField("age", label="Âge", min=18, max=99),
        SelectField("pays", label="Pays", options=["Côte d'Ivoire", "Sénégal", "France"]),
        DateField("birthday", label="Date de naissance"),
        CheckboxField("terms", label="", text="J'accepte les conditions", required=True),
        FileField("avatar", label="Photo de profil"),
    ],
    buttons=[
        {"text": "Enregistrer", "icon": "save", "variant": "primary", "type": "submit"},
        {"text": "Réinitialiser", "variant": "ghost", "type": "reset"},
    ],
    on_submit=create_user,
)
```

### Méthodes

| Méthode | Description |
|---------|-------------|
| `values()` | Renvoie un dict `{name: valeur}` |
| `set_values(data)` | Pré-remplit les champs depuis un dict |
| `get_field(name)` | Renvoie le champ par son nom |
| `validate()` | Valide tous les champs, retourne bool |
| `submit()` | Valide → appel `on_submit(values)` si valide |
| `clear()` | Réinitialise les champs |

## Champs

| Champ | TypeError | Validation spécifique |
|-------|-----------|----------------------|
| `TextField` | Texte libre | required, min_length, max_length, pattern |
| `PasswordField` | Texte masqué | idem TextField |
| `EmailField` | Texte | + format email |
| `NumberField` | int/float | + min, max, format numérique |
| `SelectField` | Choix unique | required |
| `CheckboxField` | bool | required (coché) |
| `DateField` | Date AAAA-MM-JJ | format + date valide |
| `FileField` | Chemin fichier | Dialogue "Parcourir" |

### Validateurs communs

```python
TextField("name", required=True, min_length=3, max_length=50, pattern=r"^[A-Za-z]+$")
```

### Validateur personnalisé

```python
def pair(value):
    if int(value) % 2 != 0:
        raise ValidationError("Doit être pair")

TextField("nb", validator=pair)
```