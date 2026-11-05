"""Calendrier mensuel des échéances."""

import calendar
import tkinter as tk
from datetime import date
from tkinter import ttk

from todolist.domain.task import Task
from todolist.presentation.components import Card
from todolist.presentation.responsive import LayoutMode
from todolist.presentation.styles import BACKGROUND, BORDER, MUTED, PRIMARY, SURFACE, TEXT


class CalendarPage(ttk.Frame):
    MONTHS = (
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
    )
    WEEKDAYS = ("Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim")

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, style="Page.TFrame")
        today = date.today()
        self._year = today.year
        self._month = today.month
        self._tasks: list[Task] = []
        self._mode = LayoutMode.WIDE
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(self, style="Page.TFrame")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        toolbar.columnconfigure(1, weight=1)
        ttk.Button(toolbar, text="‹", command=lambda: self._change_month(-1)).grid(row=0, column=0)
        self._month_label = ttk.Label(toolbar, text="", font=("Segoe UI", 13, "bold"))
        self._month_label.grid(row=0, column=1)
        ttk.Button(toolbar, text="Aujourd'hui", command=self._go_today).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(toolbar, text="›", command=lambda: self._change_month(1)).grid(row=0, column=3)

        calendar_card = Card(
            self,
            fill=SURFACE,
            background=BACKGROUND,
            radius=16,
            padding=(14, 14),
        )
        calendar_card.grid(row=1, column=0, sticky="nsew")
        self._calendar = calendar_card.body
        for column in range(7):
            self._calendar.columnconfigure(column, weight=1, uniform="day")

        details_card = Card(
            self,
            fill="#EDEAFF",
            background=BACKGROUND,
            border_color="#EDEAFF",
            radius=12,
            padding=(16, 10),
        )
        details_card.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        self._details = tk.Label(
            details_card.body,
            text="Sélectionnez un jour pour voir ses échéances.",
            anchor="w",
            background="#EDEAFF",
            foreground=TEXT,
            font=("Segoe UI", 9),
        )
        self._details.pack(fill="x")
        self._draw_calendar()

    def render(self, tasks: list[Task]) -> None:
        self._tasks = tasks
        self._draw_calendar()

    def _draw_calendar(self) -> None:
        for child in self._calendar.winfo_children():
            child.destroy()
        self._month_label.configure(text=f"{self.MONTHS[self._month - 1]} {self._year}")
        for column, weekday in enumerate(self.WEEKDAYS):
            tk.Label(
                self._calendar,
                text=weekday.upper(),
                background=SURFACE,
                foreground=MUTED,
                font=("Segoe UI", 8, "bold"),
            ).grid(row=0, column=column, sticky="ew", pady=(2, 8))

        weeks = calendar.Calendar(firstweekday=0).monthdatescalendar(self._year, self._month)
        for row in range(1, 7):
            self._calendar.rowconfigure(row, weight=1, uniform="week")
        today = date.today()
        tasks_by_date: dict[date, list[Task]] = {}
        for task in self._tasks:
            if task.due_date:
                tasks_by_date.setdefault(task.due_date, []).append(task)

        for row, week in enumerate(weeks, start=1):
            for column, day in enumerate(week):
                in_month = day.month == self._month
                is_today = day == today
                background = "#EDEAFF" if is_today else SURFACE
                cell = tk.Frame(
                    self._calendar,
                    background=background,
                    highlightbackground=PRIMARY if is_today else "#ECEAF1",
                    highlightthickness=2 if is_today else 1,
                    padx=7,
                    pady=5,
                    cursor="hand2" if in_month else "arrow",
                )
                cell.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
                cell.columnconfigure(0, weight=1)
                foreground = TEXT if in_month else "#C4C1CC"
                day_label = tk.Label(
                    cell,
                    text=str(day.day),
                    background=background,
                    foreground=PRIMARY if is_today else foreground,
                    anchor="w",
                    font=("Segoe UI", 9, "bold" if is_today else "normal"),
                )
                day_label.grid(row=0, column=0, sticky="nw")
                day_tasks = tasks_by_date.get(day, []) if in_month else []
                if day_tasks:
                    open_count = sum(not task.completed for task in day_tasks)
                    count_label = tk.Label(
                        cell,
                        text=f"{open_count} à faire" if open_count else "✓ terminé",
                        background=background,
                        foreground="#C43D4B" if day < today and open_count else PRIMARY,
                        anchor="w",
                        font=("Segoe UI", 7, "bold"),
                    )
                    count_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
                    if self._mode is LayoutMode.WIDE:
                        title = day_tasks[0].title
                        if len(title) > 20:
                            title = title[:18] + "…"
                        tk.Label(
                            cell,
                            text=title,
                            background=background,
                            foreground=MUTED,
                            anchor="w",
                            font=("Segoe UI", 7),
                        ).grid(row=2, column=0, sticky="w", pady=(2, 0))
                if in_month:
                    for widget in (cell, *cell.winfo_children()):
                        widget.bind("<Button-1>", lambda _event, selected=day: self._select_day(selected))

    def _select_day(self, selected: date) -> None:
        tasks = [task for task in self._tasks if task.due_date == selected]
        if not tasks:
            text = f"{selected.strftime('%d/%m/%Y')}  ·  Aucune échéance"
        else:
            titles = "  •  ".join(task.title for task in tasks[:3])
            extra = f"  +{len(tasks) - 3}" if len(tasks) > 3 else ""
            text = f"{selected.strftime('%d/%m/%Y')}  ·  {titles}{extra}"
        self._details.configure(text=text)

    def _change_month(self, offset: int) -> None:
        month = self._month + offset
        if month < 1:
            self._year -= 1
            month = 12
        elif month > 12:
            self._year += 1
            month = 1
        self._month = month
        self._draw_calendar()

    def _go_today(self) -> None:
        today = date.today()
        self._year, self._month = today.year, today.month
        self._draw_calendar()
        self._select_day(today)

    def set_mode(self, mode: LayoutMode) -> None:
        if mode != self._mode:
            self._mode = mode
            self._draw_calendar()
