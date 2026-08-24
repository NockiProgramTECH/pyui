# Dialogues et notifications

## `Dialog`

### Confirmation

```python
from pyui import Dialog

Dialog.confirm("Voulez-vous supprimer ce client ?", on_confirm=delete_client)
Dialog.confirm("Confirmer ?", on_confirm=ok, on_cancel=annuler, title="Question")
```

### Messages standards

```python
Dialog.error("Impossible de se connecter au serveur")
Dialog.warning("Ce fichier existe déjà")
Dialog.success("Client enregistré avec succès")
Dialog.info("Mise à jour terminée")
```

## `Toast`

Notifications éphémères (3,5 secondes) en bas à droite.

```python
from pyui import Toast

Toast.success("Client enregistré")
Toast.error("Erreur de connexion")
Toast.warning("Stock faible")
Toast.info("Mise à jour disponible")
```

Les toasts disparaissent automatiquement. Un clic dessus les ferme immédiatement.