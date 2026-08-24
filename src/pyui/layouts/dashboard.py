"""Composants spécialisés dashboard PyUI (Niveau 11, Phase 9)."""

import tkinter as tk

from pyui.core.component import Component
from pyui.icons.manager import IconManager
from pyui.layouts.grid import Grid
from pyui.layouts.row import Row
from pyui.theme.theme import Theme
from pyui.widgets.button import Button
from pyui.widgets.card import Card
from pyui.widgets.label import Label


class StatCard(Card):
    """Carte statistique : titre, valeur, icône, tendance.

    Exemple :
        StatCard(parent, title="Clients", value="1 245", icon="users", delta="+12%")
    """

    def __init__(self, parent=None, title="", value="", icon=None, delta=None):
        self.stat_title = title
        self.stat_value = value
        self.stat_icon = icon
        self.delta = delta
        super().__init__(parent, title=title)

    def render(self):
        super().render()
        value_text = self.stat_value
        if self.stat_icon:
            glyph = IconManager.glyph(self.stat_icon)
            if glyph:
                value_text = f"{glyph}  {value_text}"
        Label(self, text=value_text, size="2xl", weight="bold").pack(fill="x", anchor="w")
        if self.delta is not None:
            color = "danger" if str(self.delta).startswith("-") else "success"
            Label(self, text=self.delta, size="sm", color=color).pack(fill="x", anchor="w")


class Chart(Component):
    """Graphique en barres ou en courbes dessiné sur Canvas.

    Exemple :
        Chart(parent, kind="bar", data={"labels": ["Jan", "Fév"], "values": [120, 180]})
    """

    _tk_class = tk.Canvas

    def __init__(self, parent=None, kind="line", data=None, title=None,
                 height=240):
        self.kind = kind if kind in ("line", "bar") else "line"
        self.chart_data = data or []
        self.chart_title = title
        self.height = height
        self._labels = []
        self._values = []
        super().__init__(parent)

    def _widget_kwargs(self, **kwargs):
        return {
            "height": self.height,
            "bg": Theme.get("surface"),
            "highlightthickness": 1,
            "highlightbackground": Theme.get("border"),
            "bd": 0,
            **super()._widget_kwargs(**kwargs),
        }

    def render(self):
        self.set_data(self.chart_data)
        if self._tk is not None:
            self._tk.bind("<Configure>", lambda e: self._draw())

    def set_data(self, data):
        """Met à jour les données du graphique et le redessine."""
        if isinstance(data, dict):
            self._labels = list(data.get("labels", []))
            self._values = list(data.get("values", []))
        else:
            self._values = list(data or [])
            self._labels = [str(i) for i in range(len(self._values))]
        self._draw()
        return self

    def _draw(self):
        if self._tk is None:
            return
        self._tk.delete("all")
        w = self._tk.winfo_width()
        h = self._tk.winfo_height()
        if w <= 2:
            w = 600
        if h <= 2:
            h = self.height

        primary = Theme.get("primary")
        text = Theme.get("text")
        muted = Theme.get("muted")
        border = Theme.get("border")
        values = self._values or [0]
        maximum = max(values) if max(values) > 0 else 1
        minimum = 0

        pad_l, pad_r, pad_t, pad_b = 44, 16, 24, 28
        plot_w = w - pad_l - pad_r
        plot_h = h - pad_t - pad_b

        self._tk.create_text(pad_l // 2, pad_t, text=self.chart_title or "",
                             fill=text, font=Theme.font("base", "bold"), anchor="w")

        # Grille horizontale
        steps = 4
        for i in range(steps + 1):
            y = pad_t + plot_h - (plot_h * i / steps)
            self._tk.create_line(pad_l, y, w - pad_r, y, fill=border)
            value = minimum + (maximum - minimum) * i / steps
            self._tk.create_text(pad_l - 6, y, text=f"{value:g}", fill=muted,
                                 font=Theme.font("xs"), anchor="e")

        n = len(values)
        if n == 0:
            return

        if self.kind == "bar":
            bar_w = plot_w / n * 0.6
            gap = plot_w / n
            for i, value in enumerate(values):
                x = pad_l + gap * i + (gap - bar_w) / 2
                hh = plot_h * value / maximum
                y0 = pad_t + plot_h - hh
                self._tk.create_rectangle(x, y0, x + bar_w, pad_t + plot_h,
                                          fill=primary, outline="")
                if i < len(self._labels):
                    self._tk.create_text(x + bar_w / 2, pad_t + plot_h + 12,
                                         text=self._labels[i], fill=muted,
                                         font=Theme.font("xs"))
        else:
            step_x = plot_w / (n - 1) if n > 1 else plot_w
            points = []
            for i, value in enumerate(values):
                x = pad_l + step_x * i
                y = pad_t + plot_h - plot_h * value / maximum
                points.append((x, y))
                self._tk.create_oval(x - 3, y - 3, x + 3, y + 3, fill=primary, outline="")
                if i < len(self._labels):
                    self._tk.create_text(x, pad_t + plot_h + 12, text=self._labels[i],
                                         fill=muted, font=Theme.font("xs"))
            for (x1, y1), (x2, y2) in zip(points, points[1:]):
                self._tk.create_line(x1, y1, x2, y2, fill=primary, width=2)

    def _apply_theme(self):
        if self._tk is not None:
            self._tk.configure(bg=Theme.get("surface"),
                               highlightbackground=Theme.get("border"))
            self._draw()


class Activity(Component):
    """Flux d'activités récentes.

    items = [{"icon": "user", "text": "...", "time": "il y a 5 min", "color": "primary"}]
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, items=None):
        self.items = list(items or [])
        self._rows = []
        super().__init__(parent)

    def render(self):
        for item in self.items:
            row = tk.Frame(self._tk, bg=Theme.get("surface"))
            row.pack(fill="x", pady=3)
            icon = item.get("icon")
            glyph = IconManager.glyph(icon) if icon else "\u2022"
            tk.Label(row, text=glyph, bg=Theme.get("surface"),
                     fg=Theme.get(item.get("color", "primary")),
                     font=("Segoe UI Emoji", 12)).pack(side="left", padx=(0, 8))
            tk.Label(row, text=item.get("text", ""), bg=Theme.get("surface"),
                     fg=Theme.get("text"), font=Theme.font("base"),
                     anchor="w", justify="left").pack(side="left", fill="x", expand=True)
            if item.get("time"):
                tk.Label(row, text=item["time"], bg=Theme.get("surface"),
                         fg=Theme.get("muted"), font=Theme.font("xs")).pack(side="right")
            self._rows.append(row)

    def _apply_theme(self):
        if self._tk is None:
            return
        bg = Theme.get("surface")
        self._tk.configure(bg=bg)
        for row in self._rows:
            row.configure(bg=bg)
            for child in row.winfo_children():
                child.configure(bg=bg)


class Timeline(Component):
    """Chronologie verticale d'événements.

    items = [{"title": "...", "time": "...", "text": "..."}]
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, items=None):
        self.items = list(items or [])
        self._rows = []
        super().__init__(parent)

    def render(self):
        for item in self.items:
            row = tk.Frame(self._tk, bg=Theme.get("surface"))
            row.pack(fill="x", anchor="n")
            dot = tk.Label(row, text="\u25CF", bg=Theme.get("surface"),
                           fg=Theme.get(item.get("color", "primary")),
                           font=Theme.font("sm"))
            dot.pack(side="left", padx=(0, 8), pady=(4, 0))
            content = tk.Frame(row, bg=Theme.get("surface"))
            content.pack(side="left", fill="x", expand=True)
            title_row = tk.Frame(content, bg=Theme.get("surface"))
            title_row.pack(fill="x")
            tk.Label(title_row, text=item.get("title", ""), bg=Theme.get("surface"),
                     fg=Theme.get("text"), font=Theme.font("base", "bold"),
                     anchor="w").pack(side="left")
            if item.get("time"):
                tk.Label(title_row, text=item["time"], bg=Theme.get("surface"),
                         fg=Theme.get("muted"), font=Theme.font("xs")).pack(side="right")
            if item.get("text"):
                tk.Label(content, text=item["text"], bg=Theme.get("surface"),
                         fg=Theme.get("muted"), font=Theme.font("sm"),
                         anchor="w", justify="left").pack(fill="x", pady=(2, 0))
            self._rows.append(row)

    def _apply_theme(self):
        if self._tk is None:
            return
        bg = Theme.get("surface")
        self._tk.configure(bg=bg)
        for row in self._rows:
            row.configure(bg=bg)
            for child in row.winfo_children():
                child.configure(bg=bg)


class QuickAction(Button):
    """Action rapide cliquable avec icône."""

    def __init__(self, parent=None, text="", icon=None, command=None):
        super().__init__(parent, text=text, icon=icon, command=command,
                         variant="outline")


class Metric(Component):
    """Métrique : grande valeur + étiquette."""

    _tk_class = tk.Frame

    def __init__(self, parent=None, label="", value=""):
        self.metric_label = label
        self.metric_value = value
        super().__init__(parent)

    def render(self):
        Label(self, text=self.metric_value, size="xl", weight="bold").pack(anchor="w")
        Label(self, text=self.metric_label, size="sm", color="muted").pack(anchor="w")

    def _apply_theme(self):
        self._apply_bg("background")


class Dashboard(Component):
    """Composition prête à l'emploi : stats + graphique + activités + actions.

    Exemple :
        Dashboard(parent, stats=[...], chart={"kind": "bar", "data": {...}},
                  activity=[...], actions=[{"text": "Nouveau", "icon": "plus", "command": f}])
    """

    _tk_class = tk.Frame

    def __init__(self, parent=None, stats=None, chart=None, activity=None,
                 actions=None, timeline=None, columns=4):
        self.stats = list(stats or [])
        self.chart_spec = chart
        self.activity_items = list(activity or [])
        self.action_specs = list(actions or [])
        self.timeline_items = list(timeline or [])
        self.columns = max(2, columns)
        super().__init__(parent)

    def render(self):
        from pyui.widgets.frame import Frame

        if self.stats:
            grid = Grid(self, columns=self.columns, spacing=8)
            for spec in self.stats:
                grid.add(StatCard, **spec)
            grid.pack(fill="x", pady=(0, 12))

        body = Frame(self, padding=0)
        body.pack(fill="both", expand=True)

        left = Frame(body, padding=0)
        left.pack(side="left", fill="both", expand=True)

        if self.chart_spec:
            Chart(left, kind=self.chart_spec.get("kind", "line"),
                  data=self.chart_spec.get("data"),
                  title=self.chart_spec.get("title"),
                  height=self.chart_spec.get("height", 240)).pack(fill="both", expand=True, padx=(0, 8))

        if self.timeline_items:
            Timeline(left, items=self.timeline_items).pack(fill="x", pady=(12, 0))

        right = Frame(body, padding=0)
        right.pack(side="right", fill="y")

        if self.activity_items:
            Activity(right, items=self.activity_items).pack(fill="x", padx=(8, 0))

        if self.action_specs:
            actions = Row(right, spacing=8)
            actions.pack(fill="x", padx=(8, 0), pady=(12, 0))
            for spec in self.action_specs:
                actions.add(QuickAction, text=spec.get("text", ""),
                            icon=spec.get("icon"), command=spec.get("command"))

    def _apply_theme(self):
        self._apply_bg()