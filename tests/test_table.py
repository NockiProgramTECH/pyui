"""Tests du DataTable (Niveau 6)."""

import os


def make_data(n):
    return [{"id": i, "name": f"Client {i}", "ville": "Abidjan" if i % 2 else "Dakar"}
            for i in range(n)]


def test_table_creation_and_rows(app):
    from pyui import DataTable

    table = DataTable(app, columns=[("id", "ID"), ("name", "Nom")], data=make_data(5))
    assert len(table.data) == 5
    assert table._tree.get_children() != ()


def test_table_requires_columns(app):
    from pyui import DataTable
    import pytest

    with pytest.raises(ValueError):
        DataTable(app, columns=[])


def test_table_search(app):
    from pyui import DataTable
    from pyui.widgets.input import Input

    table = DataTable(app, columns=[("id", "ID"), ("name", "Nom")], data=make_data(5))
    table._search_text = "Client 3"
    table.refresh()
    rows = table._tree.get_children()
    assert len(rows) == 1
    assert table._tree.item(rows[0], "values")[1] == "Client 3"


def test_table_sort(app):
    from pyui import DataTable

    table = DataTable(app, columns=[("id", "ID"), ("name", "Nom")], data=make_data(4))
    table._sort_key = "id"
    table._sort_reverse = True
    table.refresh()
    rows = table._tree.get_children()
    assert table._tree.item(rows[0], "values")[0] == "3"


def test_table_pagination(app):
    from pyui import DataTable

    table = DataTable(app, columns=[("id", "ID")], data=make_data(12), page_size=5)
    assert len(table._tree.get_children()) == 5
    table.next_page()
    assert table._page == 2
    assert len(table._tree.get_children()) == 5
    table.next_page()
    assert table._page == 3
    assert len(table._tree.get_children()) == 2
    table.next_page()  # au-delà de la dernière page
    assert table._page == 3


def test_table_previous_page_disabled(app):
    from pyui import DataTable

    table = DataTable(app, columns=[("id", "ID")], data=make_data(12), page_size=5)
    assert table._page == 1
    table.previous_page()
    assert table._page == 1


def test_table_selection(app):
    from pyui import DataTable

    selected = []
    table = DataTable(app, columns=[("id", "ID"), ("name", "Nom")],
                      data=make_data(3), on_select=lambda rows: selected.append(rows))
    children = table._tree.get_children()
    table._tree.selection_set(children[1])
    table._on_tree_select(None)
    assert selected and selected[0][0]["name"] == "Client 1"


def test_table_double_click(app):
    from pyui import DataTable

    double_clicked = []
    table = DataTable(app, columns=[("id", "ID"), ("name", "Nom")],
                      data=make_data(3), on_double_click=lambda row: double_clicked.append(row))
    children = table._tree.get_children()

    class FakeEvent:
        y = 0

    table._tree.identify_row = lambda y: children[0]
    table._on_double_click(FakeEvent())
    assert double_clicked and double_clicked[0]["name"] == "Client 0"


def test_table_export_csv(app, tmp_path):
    from pyui import DataTable

    table = DataTable(app, columns=[("id", "ID"), ("name", "Nom")], data=make_data(3))
    path = tmp_path / "export.csv"
    result = table.export(str(path))
    assert os.path.exists(result)
    content = path.read_text(encoding="utf-8-sig")
    assert "ID" in content and "Client 0" in content


def test_table_remove_row(app):
    from pyui import DataTable

    table = DataTable(app, columns=[("id", "ID"), ("name", "Nom")], data=make_data(3))
    table.remove_row(lambda r: r["id"] == 1)
    assert len(table.data) == 2


def test_table_column_class(app):
    from pyui import DataTable, TableColumn

    table = DataTable(app, columns=[TableColumn("id", "ID", width=80),
                                    TableColumn("name", "Nom", width=200)],
                      data=make_data(2))
    assert len(table.columns) == 2
    assert table.columns[1].width == 200