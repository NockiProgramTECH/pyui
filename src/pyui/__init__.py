"""PyUI — Framework GUI desktop Python au-dessus de Tkinter/ttk."""

from pyui.core.app import App
from pyui.core.component import Component
from pyui.core.events import Event, EventBus
from pyui.core.router import Router
from pyui.core.state import State
from pyui.core.page import Page
from pyui.core.placement import Pack, Grid as GridPlacement, Place

from pyui.widgets.button import Button
from pyui.widgets.label import Label
from pyui.widgets.input import Input
from pyui.widgets.text import Text
from pyui.widgets.checkbox import CheckBox
from pyui.widgets.radio import RadioButton
from pyui.widgets.select import Select
from pyui.widgets.listbox import ListBox
from pyui.widgets.progressbar import ProgressBar
from pyui.widgets.separator import Separator
from pyui.widgets.frame import Frame
from pyui.widgets.card import Card
from pyui.widgets.badge import Badge
from pyui.widgets.alert import Alert
from pyui.widgets.tooltip import Tooltip
from pyui.widgets.modal import Modal
from pyui.widgets.loading import Loading
from pyui.widgets.spinner import Spinner
from pyui.widgets.accordion import Accordion
from pyui.widgets.tabs import Tabs

from pyui.layouts.container import Container
from pyui.layouts.stack import Stack
from pyui.layouts.row import Row
from pyui.layouts.column import Column
from pyui.layouts.grid import Grid
from pyui.layouts.sidebar import Sidebar
from pyui.layouts.navbar import Navbar
from pyui.layouts.footer import Footer
from pyui.layouts.dashboard import Dashboard, StatCard, Chart, Activity, Timeline, QuickAction, Metric

from pyui.forms.form import Form
from pyui.forms.fields import (
    FormField, TextField, PasswordField, NumberField,
    EmailField, SelectField, CheckboxField, DateField, FileField,
)

from pyui.tables.table import DataTable
from pyui.tables.columns import Column as TableColumn
from pyui.tables.filters import Filter
from pyui.tables.pagination import Pagination

from pyui.theme.theme import Theme
from pyui.theme import colors as theme_colors

from pyui.icons.manager import IconManager, GLYPHS

from pyui.dialogs.dialog import Dialog, ConfirmDialog, ErrorDialog, SuccessDialog, WarningDialog
from pyui.notifications.toast import Toast
from pyui.notifications.notification import Notification

__version__ = "0.1.0"

__all__ = [
    "App", "Component", "Event", "EventBus", "Router", "State", "Page",
    "Pack", "GridPlacement", "Place",
    "Button", "Label", "Input", "Text", "CheckBox", "RadioButton",
    "Select", "ListBox", "ProgressBar", "Separator", "Frame", "Card", "Badge",
    "Alert", "Tooltip", "Modal", "Loading", "Spinner", "Accordion", "Tabs",
    "Container", "Stack", "Row", "Column", "Grid", "Sidebar", "Navbar",
    "Footer", "Dashboard", "StatCard", "Chart", "Activity", "Timeline",
    "QuickAction", "Metric",
    "Form", "FormField", "TextField", "PasswordField", "NumberField",
    "EmailField", "SelectField", "CheckboxField", "DateField", "FileField",
    "DataTable", "TableColumn", "Filter", "Pagination",
    "Theme", "theme_colors", "IconManager", "GLYPHS",
    "Dialog", "ConfirmDialog", "ErrorDialog", "SuccessDialog", "WarningDialog",
    "Toast", "Notification",
    "__version__",
]