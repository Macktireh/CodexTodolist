"""Page regroupant les tâches à échéance proche."""

import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk
from typing import TYPE_CHECKING

from todolist.domain.task import Task, TaskPriority
from todolist.presentation.components import Card
from todolist.presentation.responsive import LayoutMode
from todolist.presentation.styles import BACKGROUND, BORDER, MUTED, SURFACE

if TYPE_CHECKING:
    from todolist.presentation.task_controller import TaskController


class TodayPage(ttk.Frame):
    PRIORITY_LABELS = {
        TaskPriority.LOW: "Basse",
        TaskPriority.NORMAL: "Normale",
        TaskPriority.HIGH: "Haute",
        TaskPriority.URGENT: "Urgente",
    }

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, style="Page.TFrame")
        self._controller: TaskController | None = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        summary = ttk.Frame(self, style="Page.TFrame")
        summary.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        summary.columnconfigure((0, 1, 2), weight=1)
        self._overdue = self._metric(summary, 0, "En retard", "#FCE8EA", "#C43D4B")
        self._today = self._metric(summary, 1, "Aujourd'hui", "#FAEDE2", "#C96B20")
        self._upcoming = self._metric(summary, 2, "7 prochains jours", "#EDEAFF", "#6757D9")

        card = Card(
            self,
            fill=SURFACE,
            background=BACKGROUND,
            radius=16,
            padding=(20, 18),
        )
        card.grid(row=1, column=0, sticky="nsew")
        body = card.body
        body.columnconfigure(0, weight=1)
        body.rowconfigure(2, weight=1)
        tk.Label(
            body,
            text="Échéances à surveiller",
            background=SURFACE,
            foreground="#172033",
            font=("Segoe UI", 12, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            body,
            text="Double-cliquez sur une tâche pour la modifier.",
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, sticky="w", pady=(3, 12))

        self._tree = ttk.Treeview(
            body,
            columns=("priority", "title", "category", "due"),
            show="headings",
            style="Tasks.Treeview",
            selectmode="browse",
        )
        self._tree.heading("priority", text="PRIORITÉ")
        self._tree.heading("title", text="TÂCHE")
        self._tree.heading("category", text="CATÉGORIE")
        self._tree.heading("due", text="ÉCHÉANCE")
        self._tree.column("priority", width=95, minwidth=75, stretch=False)
        self._tree.column("title", width=300, minwidth=160)
        self._tree.column("category", width=130, minwidth=80)
        self._tree.column("due", width=120, minwidth=95, stretch=False)
        self._tree.tag_configure("overdue", foreground="#C43D4B")
        self._tree.tag_configure("today", foreground="#C96B20")
        self._tree.tag_configure("odd", background="#F8F7FB")
        self._tree.grid(row=2, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=self._tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self._tree.configure(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(self, style="Page.TFrame")
        actions.grid(row=2, column=0, sticky="e", pady=(12, 0))
        ttk.Button(actions, text="Modifier", command=self._edit_selected).pack(side="left")
        ttk.Button(
            actions,
            text="Valider",
            style="Primary.TButton",
            command=self._complete_selected,
        ).pack(side="left", padx=(8, 0))

    @staticmethod
    def _metric(parent: ttk.Frame, column: int, title: str, background: str, color: str) -> tk.Label:
        card = Card(
            parent,
            fill=background,
            background=BACKGROUND,
            border_color=background,
            radius=12,
            padding=(15, 11),
        )
        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=(0 if column == 0 else 5, 0 if column == 2 else 5),
        )
        body = card.body
        value = tk.Label(
            body,
            text="0",
            background=background,
            foreground=color,
            font=("Segoe UI", 18, "bold"),
        )
        value.pack(side="left")
        tk.Label(
            body,
            text=title,
            background=background,
            foreground=color,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(9, 0))
        return value

    def set_controller(self, controller: "TaskController") -> None:
        self._controller = controller
        self._tree.bind("<Double-1>", lambda _event: self._edit_selected())
        self._tree.bind("<space>", lambda _event: self._complete_selected())

    def render(self, tasks: list[Task]) -> None:
        today = date.today()
        active = [task for task in tasks if not task.completed and task.due_date]
        overdue = [task for task in active if task.due_date < today]
        due_today = [task for task in active if task.due_date == today]
        upcoming = [task for task in active if today < task.due_date <= today + timedelta(days=7)]
        self._overdue.configure(text=str(len(overdue)))
        self._today.configure(text=str(len(due_today)))
        self._upcoming.configure(text=str(len(upcoming)))
        visible = sorted(overdue + due_today + upcoming, key=lambda task: task.due_date or today)
        self._tree.delete(*self._tree.get_children())
        for index, task in enumerate(visible):
            tags = ["odd"] if index % 2 else []
            if task.due_date and task.due_date < today:
                tags.append("overdue")
                due_label = f"En retard · {task.due_date.strftime('%d/%m')}"
            elif task.due_date == today:
                tags.append("today")
                due_label = "Aujourd'hui"
            else:
                due_label = task.due_date.strftime("%d/%m/%Y") if task.due_date else "—"
            self._tree.insert(
                "",
                "end",
                iid=task.id,
                values=(self.PRIORITY_LABELS[task.priority], task.title, task.category, due_label),
                tags=tuple(tags),
            )

    def _selected_id(self) -> str | None:
        selection = self._tree.selection()
        return selection[0] if selection else None

    def _edit_selected(self) -> None:
        task_id = self._selected_id()
        if task_id and self._controller:
            self._controller.edit_task(task_id)

    def _complete_selected(self) -> None:
        task_id = self._selected_id()
        if task_id and self._controller:
            self._controller.toggle_task(task_id)

    def set_mode(self, mode: LayoutMode) -> None:
        narrow = mode is LayoutMode.NARROW
        self._tree.column("category", width=0 if narrow else 130, stretch=not narrow)
