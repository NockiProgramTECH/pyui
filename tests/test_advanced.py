"""Tests des widgets avancés (Niveau 2) et du Dashboard (Phase 9)."""

import pytest


def test_badge(app):
    from pyui import Badge

    badge = Badge(app, text="Actif", variant="success")
    assert badge.text == "Actif"
    badge.text = "Inactif"
    assert badge.tk.cget("text") == "Inactif"


def test_alert(app):
    from pyui import Alert

    alert = Alert(app, message="Erreur", variant="danger", dismissible=True)
    assert alert.message == "Erreur"
    alert.hide()
    assert alert._visible is False


def test_tooltip(app):
    from pyui import Button, Tooltip

    button = Button(app, text="OK")
    tip = Tooltip(button, text="Aide", delay=100)
    assert tip.tooltip_text == "Aide"


def test_spinner(app):
    from pyui import Spinner

    spinner = Spinner(app, size=24)
    spinner.start()
    assert spinner._running is True
    spinner.stop()
    assert spinner._running is False


def test_loading(app):
    from pyui import Loading

    loading = Loading(app, message="Chargement...")
    loading.open()
    assert loading._visible is True
    loading.close()
    assert loading._visible is False


def test_tabs_select(app):
    from pyui import Tabs, Label

    tabs = Tabs(app, tabs=[
        {"text": "A", "content": lambda p: Label(p, text="Contenu A")},
        {"text": "B", "content": lambda p: Label(p, text="Contenu B")},
    ])
    assert tabs.index == 0
    tabs.select(1)
    assert tabs.index == 1


def test_accordion_toggle(app):
    from pyui import Accordion, Label

    acc = Accordion(app, sections=[
        {"title": "S1", "content": lambda p: Label(p, text="c1")},
    ])
    assert acc._items[0]["expanded"] is False
    acc.toggle(0)
    assert acc._items[0]["expanded"] is True
    acc.toggle(0)
    assert acc._items[0]["expanded"] is False


def test_modal(app):
    from pyui import Modal, Label

    modal = Modal(app, title="Test", content=lambda p: Label(p, text="Contenu"))
    win = modal.open()
    assert win is not None
    modal.close()
    assert modal._win is None


def test_chart_bar(app):
    from pyui import Chart

    chart = Chart(app, kind="bar", data={"labels": ["A", "B"], "values": [1, 2]})
    assert chart._values == [1, 2]
    chart.set_data([5, 6, 7])
    assert chart._values == [5, 6, 7]


def test_chart_line(app):
    from pyui import Chart

    chart = Chart(app, kind="line", data=[10, 20])
    assert chart._values == [10, 20]


def test_statcard(app):
    from pyui import StatCard

    card = StatCard(app, title="Clients", value="1 245", icon="users", delta="+12%")
    assert card.stat_title == "Clients"
    assert card.stat_value == "1 245"
    assert len(card.children) >= 3  # titre + valeur + delta


def test_activity(app):
    from pyui import Activity

    activity = Activity(app, items=[
        {"icon": "user", "text": "Nouveau", "time": "il y a 5 min"},
    ])
    assert len(activity.items) == 1


def test_timeline(app):
    from pyui import Timeline

    timeline = Timeline(app, items=[
        {"title": "Livré", "time": "14:30", "text": "Détails"},
    ])
    assert len(timeline.items) == 1


def test_quickaction(app):
    from pyui import QuickAction

    clicked = []

    def cmd():
        clicked.append(1)

    QuickAction(app, text="Nouveau", icon="plus", command=cmd).tk.invoke()
    assert clicked == [1]


def test_metric(app):
    from pyui import Metric

    metric = Metric(app, label="CA", value="2 450 000 FCFA")
    assert metric.metric_value == "2 450 000 FCFA"


def test_dashboard_composition(app):
    from pyui import Dashboard

    dash = Dashboard(
        app,
        stats=[
            {"title": "Clients", "value": "1 245", "icon": "users"},
            {"title": "Ventes", "value": "86", "icon": "chart"},
        ],
        chart={"kind": "bar", "data": {"labels": ["A", "B"], "values": [1, 2]}},
        activity=[{"icon": "user", "text": "x", "time": "y"}],
        actions=[{"text": "Exporter", "icon": "download"}],
    )
    assert len(dash.stats) == 2
    assert dash.chart_spec["kind"] == "bar"
    app.tk.update()