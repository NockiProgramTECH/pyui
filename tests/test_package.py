"""Tests de packaging : version, exports publics, installabilité."""

import pyui


def test_version():
    assert pyui.__version__ == "0.1.0"


def test_all_names_importable():
    """Chaque nom de __all__ doit être résolvable depuis le package."""
    for name in pyui.__all__:
        assert hasattr(pyui, name), f"Nom manquant : {name}"


def test_public_exports():
    from pyui import App, Button, Card, Column, DataTable, Form, Label
    from pyui import Sidebar, Navbar, Theme, State, Router, Page
    from pyui import Dashboard, Chart, StatCard, Tabs, Modal, Toast, Dialog

    assert App and Button and Card and Column and DataTable
    assert Form and Label and Sidebar and Navbar and Theme
    assert State and Router and Page and Dashboard and Chart
    assert StatCard and Tabs and Modal and Toast and Dialog


def test_key_examples_import():
    import importlib

    modules = [
        "examples.01_hello",
        "examples.03_app_shell",
        "examples.04_forms",
        "examples.05_table",
        "examples.06_gest_clients",
        "examples.07_dashboard",
        "examples.08_state",
    ]
    for name in modules:
        mod = importlib.import_module(name)
        assert mod is not None