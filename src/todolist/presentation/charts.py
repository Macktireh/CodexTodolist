"""Graphiques Matplotlib intégrés dans l'interface Tkinter."""

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from todolist.presentation.styles import MUTED, PRIMARY, SUCCESS, SURFACE, TEXT


class DonutChart(tk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, background=SURFACE)
        self._figure = Figure(figsize=(3.0, 2.5), dpi=100, facecolor=SURFACE)
        self._axes = self._figure.add_subplot(111)
        self._canvas = FigureCanvasTkAgg(self._figure, master=self)
        self._canvas.get_tk_widget().configure(background=SURFACE, highlightthickness=0)
        self._canvas.get_tk_widget().pack(fill="both", expand=True)
        self.set_data(0, 0)

    def set_data(self, completed: int, total: int) -> None:
        self._axes.clear()
        self._axes.set_facecolor(SURFACE)
        active = max(total - completed, 0)
        values = [completed, active] if total else [0, 1]
        colors = [SUCCESS, "#EAE8F1"] if total else ["#EAE8F1", "#EAE8F1"]
        self._axes.pie(
            values,
            colors=colors,
            startangle=90,
            counterclock=False,
            wedgeprops={"width": 0.23, "edgecolor": SURFACE, "linewidth": 2},
        )
        percent = round(completed / total * 100) if total else 0
        self._axes.text(
            0,
            0.08,
            f"{percent}%",
            ha="center",
            va="center",
            fontsize=23,
            fontweight="bold",
            color=TEXT,
        )
        self._axes.text(
            0,
            -0.18,
            "accompli",
            ha="center",
            va="center",
            fontsize=9,
            color=MUTED,
        )
        self._axes.set_aspect("equal")
        self._figure.subplots_adjust(left=0.05, right=0.95, top=0.96, bottom=0.04)
        self._canvas.draw_idle()


class BarChart(tk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, background=SURFACE)
        self._figure = Figure(figsize=(6.0, 3.0), dpi=100, facecolor=SURFACE)
        self._axes = self._figure.add_subplot(111)
        self._canvas = FigureCanvasTkAgg(self._figure, master=self)
        self._canvas.get_tk_widget().configure(background=SURFACE, highlightthickness=0)
        self._canvas.get_tk_widget().pack(fill="both", expand=True)

    def set_values(self, values: list[tuple[str, int]]) -> None:
        self._axes.clear()
        self._axes.set_facecolor(SURFACE)
        labels = [label for label, _value in values]
        counts = [value for _label, value in values]
        positions = list(range(len(values)))
        colors = ["#B5ACF1"] * max(len(values) - 1, 0) + ([PRIMARY] if values else [])
        bars = self._axes.bar(positions, counts, color=colors, width=0.58, zorder=3)
        self._axes.bar_label(
            bars,
            labels=[str(value) if value else "" for value in counts],
            padding=4,
            fontsize=8,
            color=TEXT,
            fontweight="bold",
        )
        self._axes.set_xticks(positions, labels)
        self._axes.tick_params(axis="x", colors=MUTED, labelsize=9, length=0, pad=8)
        self._axes.tick_params(axis="y", colors=MUTED, labelsize=8, length=0)
        self._axes.yaxis.grid(True, color="#EEECF4", linewidth=1, zorder=0)
        self._axes.set_axisbelow(True)
        maximum = max(counts, default=0)
        self._axes.set_ylim(0, max(maximum * 1.28, 1))
        for spine in self._axes.spines.values():
            spine.set_visible(False)
        self._figure.subplots_adjust(left=0.08, right=0.98, top=0.90, bottom=0.17)
        self._canvas.draw_idle()
