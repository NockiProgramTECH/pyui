"""Moteur de rendu Tkinter : isolé pour permettre d'autres backends (Niveau 24).

L'API publique de PyUI ne doit pas dépendre directement de Tkinter.
"""


def create_widget(kind, parent, **kwargs):
    """Crée un widget Tkinter natif à partir d'un type générique."""
