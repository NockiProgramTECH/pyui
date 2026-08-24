"""Tests des widgets de base."""


def test_button_creation_and_variants(app):
    from pyui import Button

    button = Button(app, text="Enregistrer", variant="primary")
    assert button.text == "Enregistrer"
    assert button.variant == "primary"
    assert button.tk is not None


def test_button_text_update(app):
    from pyui import Button

    button = Button(app, text="A")
    button.text = "B"
    assert button.tk.cget("text") == "B"


def test_button_command(app):
    from pyui import Button

    calls = []

    def cmd():
        calls.append(1)

    button = Button(app, text="OK", command=cmd)
    button.tk.invoke()
    assert calls == [1]


def test_input_value_and_placeholder(app):
    from pyui import Input

    entry = Input(app, value="42")
    assert entry.get() == "42"
    entry.set("99")
    assert entry.get() == "99"


def test_checkbox_state(app):
    from pyui import CheckBox

    box = CheckBox(app, text="Actif", checked=True)
    assert box.is_checked is True
    box.is_checked = False
    assert box.is_checked is False


def test_radio_groups(app):
    from pyui import RadioButton

    a = RadioButton(app, text="A", value="a", group="g")
    b = RadioButton(app, text="B", value="b", group="g")
    a.is_selected = True
    assert a.is_selected is True
    assert b.is_selected is False


def test_select_options(app):
    from pyui import Select

    select = Select(app, options=["X", "Y"], value="X")
    assert select.get() == "X"
    select.set("Y")
    assert select.get() == "Y"


def test_text_widget(app):
    from pyui import Text

    text = Text(app, value="ligne 1")
    assert text.get() == "ligne 1"
    text.set("autre")
    assert text.get() == "autre"


def test_progressbar(app):
    from pyui import ProgressBar

    bar = ProgressBar(app, value=20, maximum=100)
    bar.set(50)
    assert bar.tk.cget("value") == 50


def test_card_children(app):
    from pyui import Card, Button

    card = Card(app, title="Carte", subtitle="Sous-titre")
    Button(card, text="Action")
    assert len(card.children) >= 3  # titre + sous-titre + bouton


def test_layouts(app):
    from pyui import Row, Column, Grid, Stack, Button

    row = Row(app, spacing=4)
    row.add(Button, text="A").add(Button, text="B")
    assert len(row.children) == 2

    col = Column(app, spacing=4)
    Button(col, text="C")
    assert len(col.children) == 1

    grid = Grid(app, columns=2, spacing=4)
    grid.add(Button, text="1").add(Button, text="2").add(Button, text="3")
    assert len(grid.children) == 3

    stack = Stack(app, spacing=4)
    Button(stack, text="S")
    assert len(stack.children) == 1