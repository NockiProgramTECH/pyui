"""Tests de la gestion d'état réactif (Phase 10)."""

import pytest


def test_state_get_set():
    from pyui import State

    state = State({"count": 0, "theme": "light"})
    assert state.get("count") == 0
    assert state.get("inconnu", "défaut") == "défaut"
    state.set("count", 5)
    assert state.get("count") == 5


def test_state_subscribe_all():
    from pyui import State

    state = State({"a": 1, "b": 2})
    events = []
    state.subscribe(lambda key, value, old: events.append((key, value)))
    state.set("a", 10)
    state.set("b", 20)
    assert events == [("a", 10), ("b", 20)]


def test_state_subscribe_key():
    from pyui import State

    state = State({"a": 1, "b": 2})
    events = []
    state.subscribe("a", lambda key, value, old: events.append(value))
    state.set("a", 10)
    state.set("b", 99)  # ne doit pas déclencher
    assert events == [10]


def test_state_subscribe_noop_same_value():
    from pyui import State

    state = State({"a": 1})
    events = []
    state.subscribe(lambda key, value, old: events.append(value))
    state.set("a", 1)
    assert events == []


def test_state_unsubscribe():
    from pyui import State

    state = State({"a": 1})
    events = []
    unsub = state.subscribe("a", lambda k, v, o: events.append(v))
    state.set("a", 2)
    unsub()
    state.set("a", 3)
    assert events == [2]


def test_state_update_snapshot_reset():
    from pyui import State

    state = State({"a": 1, "b": 2})
    state.update(a=10, b=20)
    assert state.snapshot() == {"a": 10, "b": 20}
    state.reset()
    assert state.snapshot() == {"a": 1, "b": 2}


def test_state_bind_component(app):
    from pyui import State, Label

    state = State({"count": 0})
    label = Label(app, text="0")
    label.bind_state(state, "count", "text")

    state.set("count", 42)
    assert label.tk.cget("text") == 42
    state.set("count", "hello")
    assert label.tk.cget("text") == "hello"


def test_state_bind_callable(app):
    from pyui import State, Button

    state = State({"enabled": True})
    button = Button(app, text="B")
    button.bind_state(state, "enabled", lambda b, v: b.enable() if v else b.disable())

    state.set("enabled", False)
    assert button.tk.cget("state") == "disabled"
    state.set("enabled", True)
    assert button.tk.cget("state") == "normal"


def test_state_bind_unsubscribes_on_destroy(app):
    from pyui import State, Label

    state = State({"count": 0})
    label = Label(app, text="0")
    label.bind_state(state, "count", "text")
    label.destroy()

    events = []
    state.subscribe(lambda k, v, o: events.append(v))
    state.set("count", 5)  # ne doit pas lever d'erreur après destruction
    assert events == [5]


def test_state_autoupdate_label(app):
    from pyui import State, Label

    state = State({"user": "Personne"})
    label = Label(app, text="")
    label.bind_state(state, "user", "text")
    state.set("user", "Awa")
    assert label.text == "Awa"