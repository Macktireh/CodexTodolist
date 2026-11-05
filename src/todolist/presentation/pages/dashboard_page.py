"""Dashboard dense présentant les informations immédiatement utiles."""

import tkinter as tk
from tkinter import ttk

from todolist.domain.task import Task
from todolist.presentation.charts import DonutChart
from todolist.presentation.components import Card
from todolist.presentation.responsive import LayoutMode
from todolist.presentation.styles import BACKGROUND, BORDER, MUTED, PRIMARY, SUCCESS, SURFACE, TEXT


class DashboardPage(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, style="Page.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._metrics = ttk.Frame(self, style="Page.TFrame")
        self._metrics.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        self._metric_cards: list[tk.Frame] = []
        self._metric_values: dict[str, tk.Label] = {}
        definitions = (
            ("total", "TOTAL", "Toutes vos tâches", PRIMARY),
            ("active", "À FAIRE", "Restent à accomplir", "#E78B39"),
            ("completed", "TERMINÉES", "Objectifs atteints", SUCCESS),
            ("rate", "PROGRESSION", "Taux global", "#2D7DD2"),
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
                font=("Segoe UI", 21, "bold"),
            )
            value.grid(row=1, column=0, sticky="w", pady=(2, 0))
            tk.Label(
                body,
                text=caption,
                background=SURFACE,
                foreground=MUTED,
                font=("Segoe UI", 8),
            ).grid(row=2, column=0, sticky="w")
            tk.Frame(body, background=color, width=4, height=46).grid(
                row=0, column=1, rowspan=3, sticky="e"
            )
            self._metric_cards.append(card)
            self._metric_values[key] = value

        self._body = ttk.Frame(self, style="Page.TFrame")
        self._body.grid(row=1, column=0, sticky="nsew")
        self._body.columnconfigure(0, weight=5)
        self._body.columnconfigure(1, weight=3)
        self._body.rowconfigure(0, weight=1)

        self._focus_card = self._card(self._body)
        self._focus_card.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        focus_body = self._focus_card.body
        focus_body.columnconfigure(0, weight=1)
        focus_body.rowconfigure(3, weight=1)
        tk.Label(
            focus_body,
            text="À traiter maintenant",
            background=SURFACE,
            foreground=TEXT,
            font=("Segoe UI", 12, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            focus_body,
            text="Les tâches actives les plus récentes",
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, sticky="w", pady=(3, 12))
        ttk.Separator(focus_body).grid(row=2, column=0, sticky="ew")
        self._task_rows = tk.Frame(focus_body, background=SURFACE)
        self._task_rows.grid(row=3, column=0, sticky="nsew", pady=(6, 0))
        self._task_rows.columnconfigure(0, weight=1)

        self._progress_card = self._card(self._body)
        self._progress_card.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        progress_body = self._progress_card.body
        progress_body.columnconfigure(0, weight=1)
        progress_body.rowconfigure(2, weight=1)
        tk.Label(
            progress_body,
            text="Progression globale",
            background=SURFACE,
            foreground=TEXT,
            font=("Segoe UI", 12, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            progress_body,
            text="Votre rythme actuel",
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))
        self._donut = DonutChart(progress_body)
        self._donut.grid(row=2, column=0, sticky="nsew", pady=4)
        self._progress_details = tk.Label(
            progress_body,
            text="",
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 9),
        )
        self._progress_details.grid(row=3, column=0, pady=(0, 5))

        insight_card = Card(
            self,
            fill="#EDEAFF",
            background=BACKGROUND,
            border_color="#EDEAFF",
            radius=12,
            padding=(16, 10),
        )
        insight_card.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        self._insight = tk.Label(
            insight_card.body,
            text="",
            anchor="w",
            background="#EDEAFF",
            foreground=TEXT,
            font=("Segoe UI", 9, "bold"),
        )
        self._insight.pack(fill="x")
        self._place_metrics(4)

    @staticmethod
    def _card(parent: tk.Misc) -> Card:
        return Card(
            parent,
            fill=SURFACE,
            background=BACKGROUND,
            radius=16,
            padding=(20, 18),
        )

    def render(self, tasks: list[Task]) -> None:
        total = len(tasks)
        completed = sum(task.completed for task in tasks)
        active_tasks = [task for task in tasks if not task.completed]
        rate = round(completed / total * 100) if total else 0
        self._metric_values["total"].configure(text=str(total))
        self._metric_values["active"].configure(text=str(len(active_tasks)))
        self._metric_values["completed"].configure(text=str(completed))
        self._metric_values["rate"].configure(text=f"{rate}%")
        self._donut.set_data(completed, total)
        self._progress_details.configure(text=f"{completed} terminée(s)  •  {len(active_tasks)} à faire")

        for child in self._task_rows.winfo_children():
            child.destroy()
        recent = sorted(active_tasks, key=lambda task: task.created_at, reverse=True)[:6]
        if not recent:
            tk.Label(
                self._task_rows,
                text="✓  Tout est terminé, beau travail !",
                background=SURFACE,
                foreground=SUCCESS,
                font=("Segoe UI", 10, "bold"),
            ).grid(row=0, column=0, sticky="w", pady=18)
        for row, task in enumerate(recent):
            item = tk.Frame(self._task_rows, background=SURFACE, pady=7)
            item.grid(row=row, column=0, sticky="ew")
            item.columnconfigure(1, weight=1)
            tk.Label(
                item,
                text=str(row + 1),
                width=3,
                height=1,
                background="#EDEAFF",
                foreground=PRIMARY,
                font=("Segoe UI", 8, "bold"),
            ).grid(row=0, column=0, rowspan=2, padx=(0, 11))
            tk.Label(
                item,
                text=task.title,
                background=SURFACE,
                foreground=TEXT,
                anchor="w",
                font=("Segoe UI", 9, "bold"),
            ).grid(row=0, column=1, sticky="ew")
            description = task.description.replace("\n", " ")
            if len(description) > 68:
                description = description[:65] + "…"
            tk.Label(
                item,
                text=description or "Sans description",
                background=SURFACE,
                foreground=MUTED,
                anchor="w",
                font=("Segoe UI", 8),
            ).grid(row=1, column=1, sticky="ew", pady=(2, 0))
        if rate >= 70:
            message = "Excellent rythme : la majorité de vos objectifs est déjà accomplie."
        elif rate >= 40:
            message = "Vous êtes sur la bonne voie : choisissez une tâche courte pour poursuivre l'élan."
        else:
            message = "Commencez par la première priorité : une petite avancée suffit à lancer la dynamique."
        self._insight.configure(text=f"✦  {message}")

    def set_mode(self, mode: LayoutMode) -> None:
        self._place_metrics(4 if mode is LayoutMode.WIDE else 2)
        if mode is LayoutMode.NARROW:
            self._focus_card.grid_configure(row=0, column=0, padx=0, pady=(0, 12))
            self._progress_card.grid_configure(row=1, column=0, padx=0)
            self._body.columnconfigure(1, weight=0)
            self._body.rowconfigure(1, weight=1)
        else:
            self._focus_card.grid_configure(row=0, column=0, padx=(0, 7), pady=0)
            self._progress_card.grid_configure(row=0, column=1, padx=(7, 0))
            self._body.columnconfigure(1, weight=3)
            self._body.rowconfigure(1, weight=0)

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
