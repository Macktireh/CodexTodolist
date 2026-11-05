"""Page de gestion des tâches."""

import tkinter as tk
from datetime import date
from tkinter import ttk
from typing import TYPE_CHECKING

from todolist.domain.task import Task, TaskPriority
from todolist.presentation.components import Card
from todolist.presentation.responsive import LayoutMode
from todolist.presentation.styles import BACKGROUND, MUTED, SURFACE

if TYPE_CHECKING:
    from todolist.presentation.task_controller import TaskController


class TasksPage(ttk.Frame):
    FILTERS = ("Toutes", "À faire", "Terminées")
    PRIORITY_FILTERS = ("Toutes priorités", "Urgentes", "Hautes", "Normales", "Basses")
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
        self.rowconfigure(2, weight=1)

        toolbar = ttk.Frame(self, style="Page.TFrame")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        toolbar.columnconfigure(0, weight=1)
        self._search_var = tk.StringVar()
        self._search = ttk.Entry(toolbar, textvariable=self._search_var)
        self._search.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self._filter_var = tk.StringVar(value=self.FILTERS[0])
        self._filter = ttk.Combobox(
            toolbar,
            textvariable=self._filter_var,
            values=self.FILTERS,
            state="readonly",
            width=13,
        )
        self._filter.grid(row=0, column=1)
        self._priority_filter_var = tk.StringVar(value=self.PRIORITY_FILTERS[0])
        self._priority_filter = ttk.Combobox(
            toolbar,
            textvariable=self._priority_filter_var,
            values=self.PRIORITY_FILTERS,
            state="readonly",
            width=16,
        )
        self._priority_filter.grid(row=0, column=2, padx=(10, 0))
        self._refresh_button = ttk.Button(
            toolbar,
            text="↻  Actualiser",
            style="Secondary.TButton",
            command=lambda: self._controller and self._controller.reload(),
        )
        self._refresh_button.grid(row=0, column=3, padx=(10, 0))

        summary = ttk.Frame(self, style="Page.TFrame")
        summary.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        summary.columnconfigure((0, 1, 2), weight=1)
        self._all_count = self._summary_badge(summary, 0, "#EDEAFF", "#6757D9", "Toutes")
        self._active_count = self._summary_badge(summary, 1, "#FAEDE2", "#C96B20", "À faire")
        self._completed_count = self._summary_badge(summary, 2, "#E7F2ED", "#20845B", "Terminées")

        card = Card(self, fill=SURFACE, background=BACKGROUND, radius=16, padding=(18, 16))
        card.grid(row=2, column=0, sticky="nsew")
        body = card.body
        body.columnconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)
        self._count_label = ttk.Label(body, text="0 tâche", style="Count.TLabel")
        self._count_label.grid(row=0, column=0, sticky="w", pady=(0, 8))

        self._tree = ttk.Treeview(
            body,
            columns=("status", "title", "priority", "category", "due"),
            show="headings",
            style="Tasks.Treeview",
            selectmode="browse",
        )
        self._tree.heading("status", text="ÉTAT")
        self._tree.heading("title", text="TÂCHE")
        self._tree.heading("priority", text="PRIORITÉ")
        self._tree.heading("category", text="CATÉGORIE")
        self._tree.heading("due", text="ÉCHÉANCE")
        self._tree.column("status", width=90, minwidth=70, stretch=False, anchor="center")
        self._tree.column("title", width=260, minwidth=140)
        self._tree.column("priority", width=90, minwidth=0, stretch=False)
        self._tree.column("category", width=110, minwidth=0)
        self._tree.column("due", width=105, minwidth=85, stretch=False)
        self._tree.tag_configure("completed", foreground=MUTED)
        self._tree.tag_configure("urgent", foreground="#C43D4B")
        self._tree.tag_configure("overdue", foreground="#C43D4B")
        self._tree.tag_configure("odd", background="#F8F7FB")
        self._tree.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=self._tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._empty_label = tk.Label(
            body,
            text="Aucune tâche à afficher\nModifiez les filtres ou créez une nouvelle tâche.",
            justify="center",
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 10),
        )

        actions = ttk.Frame(self, style="Page.TFrame")
        actions.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        self._hint = ttk.Label(
            actions,
            text="Double-clic pour modifier • Espace pour valider",
            style="Muted.TLabel",
        )
        self._hint.pack(side="left")
        ttk.Button(
            actions,
            text="Valider / Rouvrir",
            style="Secondary.TButton",
            command=lambda: self._controller and self._controller.toggle_selected(),
        ).pack(side="right")

    @staticmethod
    def _summary_badge(
        parent: ttk.Frame,
        column: int,
        background: str,
        foreground: str,
        label: str,
    ) -> tk.Label:
        badge = Card(
            parent,
            fill=background,
            background=BACKGROUND,
            border_color=background,
            radius=12,
            padding=(13, 8),
        )
        badge.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=(0 if column == 0 else 5, 0 if column == 2 else 5),
        )
        body = badge.body
        value = tk.Label(
            body,
            text="0",
            background=background,
            foreground=foreground,
            font=("Segoe UI", 13, "bold"),
        )
        value.pack(side="left")
        tk.Label(
            body,
            text=label,
            background=background,
            foreground=foreground,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(8, 0))
        return value
        ttk.Button(
            actions,
            text="Supprimer",
            style="Danger.TButton",
            command=lambda: self._controller and self._controller.delete_selected(),
        ).pack(side="right", padx=7)
        ttk.Button(
            actions,
            text="Modifier",
            style="Secondary.TButton",
            command=lambda: self._controller and self._controller.edit_selected(),
        ).pack(side="right")

    def set_controller(self, controller: "TaskController") -> None:
        self._controller = controller
        self._search_var.trace_add("write", lambda *_args: controller.refresh())
        self._filter.bind("<<ComboboxSelected>>", lambda _event: controller.refresh())
        self._priority_filter.bind("<<ComboboxSelected>>", lambda _event: controller.refresh())
        self._tree.bind("<Double-1>", lambda _event: controller.edit_selected())
        self._tree.bind("<Delete>", lambda _event: controller.delete_selected())
        self._tree.bind("<space>", lambda _event: controller.toggle_selected())

    def render(self, tasks: list[Task], all_tasks: list[Task] | None = None) -> None:
        all_tasks = all_tasks if all_tasks is not None else tasks
        completed_count = sum(task.completed for task in all_tasks)
        self._all_count.configure(text=str(len(all_tasks)))
        self._active_count.configure(text=str(len(all_tasks) - completed_count))
        self._completed_count.configure(text=str(completed_count))
        selected = self.selected_task_id()
        self._tree.delete(*self._tree.get_children())
        for index, task in enumerate(tasks):
            tags = []
            if index % 2:
                tags.append("odd")
            if task.completed:
                tags.append("completed")
            elif task.due_date and task.due_date < date.today():
                tags.append("overdue")
            elif task.priority is TaskPriority.URGENT:
                tags.append("urgent")
            due_label = task.due_date.strftime("%d/%m/%Y") if task.due_date else "—"
            self._tree.insert(
                "",
                "end",
                iid=task.id,
                values=(
                    "✓  Terminée" if task.completed else "●  À faire",
                    task.title,
                    self.PRIORITY_LABELS[task.priority],
                    task.category,
                    due_label,
                ),
                tags=tuple(tags),
            )
        if selected and self._tree.exists(selected):
            self._tree.selection_set(selected)
        suffix = "tâche" if len(tasks) == 1 else "tâches"
        self._count_label.configure(text=f"{len(tasks)} {suffix}")
        if tasks:
            self._empty_label.place_forget()
        else:
            self._empty_label.place(relx=0.5, rely=0.55, anchor="center")

    def selected_task_id(self) -> str | None:
        selection = self._tree.selection()
        return selection[0] if selection else None

    def search_text(self) -> str:
        return self._search_var.get().strip().casefold()

    def selected_filter(self) -> str:
        return self._filter_var.get()

    def selected_priority_filter(self) -> str:
        return self._priority_filter_var.get()

    def set_mode(self, mode: LayoutMode) -> None:
        narrow = mode is LayoutMode.NARROW
        self._tree.column("priority", width=0 if narrow else 90, stretch=False)
        self._tree.column("category", width=0 if narrow else 110, stretch=not narrow)
        self._hint.pack_forget()
        if mode is LayoutMode.WIDE:
            self._hint.pack(side="left")
        self._refresh_button.configure(text="↻" if narrow else "↻  Actualiser")
        if narrow:
            self._priority_filter.grid_remove()
        else:
            self._priority_filter.grid()
