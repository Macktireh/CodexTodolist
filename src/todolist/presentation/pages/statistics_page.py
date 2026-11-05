"""Page analytique avec indicateurs et graphiques Matplotlib."""

import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk

from todolist.domain.task import Task
from todolist.presentation.charts import BarChart, DonutChart
from todolist.presentation.components import Card
from todolist.presentation.responsive import LayoutMode
from todolist.presentation.styles import BACKGROUND, BORDER, MUTED, PRIMARY, SUCCESS, SURFACE, TEXT


class StatisticsPage(ttk.Frame):
    DAY_LABELS = ("lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim.")

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, style="Page.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._metrics = ttk.Frame(self, style="Page.TFrame")
        self._metrics.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        self._metric_cards: list[tk.Frame] = []
        self._metric_values: dict[str, tk.Label] = {}
        definitions = (
            ("volume", "VOLUME", "Tâches suivies", PRIMARY),
            ("completed", "ACCOMPLIES", "Total terminé", SUCCESS),
            ("average", "MOYENNE / JOUR", "Sur 7 jours", "#2D7DD2"),
            ("best", "JOUR LE PLUS ACTIF", "Créations", "#E78B39"),
        )
        for key, title, caption, color in definitions:
            card = Card(
                self._metrics,
                fill=SURFACE,
                background=BACKGROUND,
                radius=12,
                padding=(14, 12),
            )
            body = card.body
            body.columnconfigure(0, weight=1)
            tk.Label(
                body,
                text=title,
                background=SURFACE,
                foreground=color,
                font=("Segoe UI", 8, "bold"),
            ).grid(row=0, column=0, sticky="w")
            value = tk.Label(
                body,
                text="0",
                background=SURFACE,
                foreground=TEXT,
                font=("Segoe UI", 19, "bold"),
            )
            value.grid(row=1, column=0, sticky="w", pady=(2, 0))
            tk.Label(
                body,
                text=caption,
                background=SURFACE,
                foreground=MUTED,
                font=("Segoe UI", 8),
            ).grid(row=2, column=0, sticky="w")
            self._metric_cards.append(card)
            self._metric_values[key] = value

        self._charts = ttk.Frame(self, style="Page.TFrame")
        self._charts.grid(row=1, column=0, sticky="nsew")
        self._charts.columnconfigure(0, weight=5)
        self._charts.columnconfigure(1, weight=3)
        self._charts.rowconfigure(0, weight=1)

        self._activity_card = self._make_card(
            self._charts,
            "Activité sur 7 jours",
            "Tâches ajoutées quotidiennement",
        )
        self._activity_card.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        activity_body = self._activity_card.body
        activity_body.columnconfigure(0, weight=1)
        activity_body.rowconfigure(2, weight=1)
        self._bar_chart = BarChart(activity_body)
        self._bar_chart.grid(row=2, column=0, sticky="nsew", pady=(5, 0))

        self._completion_card = self._make_card(
            self._charts,
            "Accomplissement",
            "Répartition de toutes les tâches",
        )
        self._completion_card.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        completion_body = self._completion_card.body
        completion_body.columnconfigure(0, weight=1)
        completion_body.rowconfigure(2, weight=1)
        self._donut_chart = DonutChart(completion_body)
        self._donut_chart.grid(row=2, column=0, sticky="nsew")
        legend = tk.Frame(completion_body, background=SURFACE)
        legend.grid(row=3, column=0, sticky="ew")
        legend.columnconfigure((0, 1), weight=1)
        self._active_label = self._legend_item(legend, 0, "#E78B39", "À faire")
        self._completed_label = self._legend_item(legend, 1, SUCCESS, "Terminées")

        insight_card = Card(
            self,
            fill="#E7F2ED",
            background=BACKGROUND,
            border_color="#E7F2ED",
            radius=12,
            padding=(16, 10),
        )
        insight_card.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        self._insight = tk.Label(
            insight_card.body,
            text="",
            anchor="w",
            background="#E7F2ED",
            foreground=TEXT,
            font=("Segoe UI", 9, "bold"),
        )
        self._insight.pack(fill="x")
        self._place_metrics(4)

    @staticmethod
    def _make_card(parent: tk.Misc, title: str, subtitle: str) -> Card:
        card = Card(
            parent,
            fill=SURFACE,
            background=BACKGROUND,
            radius=16,
            padding=(20, 18),
        )
        body = card.body
        tk.Label(
            body,
            text=title,
            background=SURFACE,
            foreground=TEXT,
            font=("Segoe UI", 12, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            body,
            text=subtitle,
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))
        return card

    @staticmethod
    def _legend_item(parent: tk.Frame, column: int, color: str, text: str) -> tk.Label:
        item = tk.Frame(parent, background=SURFACE)
        item.grid(row=0, column=column, sticky="w" if column == 0 else "e")
        tk.Label(item, text="●", background=SURFACE, foreground=color).pack(side="left")
        label = tk.Label(
            item,
            text=f"{text}  0",
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 8),
        )
        label.pack(side="left", padx=(3, 0))
        return label

    def render(self, tasks: list[Task]) -> None:
        total = len(tasks)
        completed = sum(task.completed for task in tasks)
        active = total - completed
        self._donut_chart.set_data(completed, total)
        self._active_label.configure(text=f"À faire  {active}")
        self._completed_label.configure(text=f"Terminées  {completed}")

        today = datetime.now().astimezone().date()
        days = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
        counts = {day: 0 for day in days}
        for task in tasks:
            task_day = task.created_at.astimezone().date()
            if task_day in counts:
                counts[task_day] += 1
        values = [(self.DAY_LABELS[day.weekday()], counts[day]) for day in days]
        self._bar_chart.set_values(values)
        weekly_total = sum(counts.values())
        best_day = max(days, key=counts.get) if days else today

        self._metric_values["volume"].configure(text=str(total))
        self._metric_values["completed"].configure(text=str(completed))
        self._metric_values["average"].configure(text=f"{weekly_total / 7:.1f}")
        self._metric_values["best"].configure(text=self.DAY_LABELS[best_day.weekday()].capitalize())

        percent = round(completed / total * 100) if total else 0
        if not total:
            message = "Ajoutez des tâches pour commencer à mesurer votre activité."
        elif percent >= 70:
            message = f"Très belle performance : {percent}% de vos tâches sont accomplies."
        elif percent >= 40:
            message = f"Progression régulière : encore {active} tâche(s) à finaliser."
        else:
            message = f"Concentrez-vous sur une priorité : {active} tâche(s) restent ouvertes."
        self._insight.configure(text=f"✦  {message}")

    def set_mode(self, mode: LayoutMode) -> None:
        self._place_metrics(4 if mode is LayoutMode.WIDE else 2)
        if mode is LayoutMode.NARROW:
            self._activity_card.grid_configure(row=0, column=0, padx=0, pady=(0, 12))
            self._completion_card.grid_configure(row=1, column=0, padx=0)
            self._charts.columnconfigure(1, weight=0)
            self._charts.rowconfigure(1, weight=1)
        else:
            self._activity_card.grid_configure(row=0, column=0, padx=(0, 7), pady=0)
            self._completion_card.grid_configure(row=0, column=1, padx=(7, 0))
            self._charts.columnconfigure(1, weight=3)
            self._charts.rowconfigure(1, weight=0)

    def _place_metrics(self, columns: int) -> None:
        for column in range(4):
            self._metrics.columnconfigure(column, weight=0)
        for index, card in enumerate(self._metric_cards):
            row, column = divmod(index, columns)
            card.grid(
                row=row,
                column=column,
                sticky="ew",
                padx=(0 if column == 0 else 5, 0 if column == columns - 1 else 5),
                pady=(0, 10) if row == 0 and columns == 2 else 0,
            )
            self._metrics.columnconfigure(column, weight=1)
