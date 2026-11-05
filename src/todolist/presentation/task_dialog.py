"""Boîte de dialogue de création et de modification d'une tâche."""

import tkinter as tk
from dataclasses import dataclass
from datetime import date
from tkinter import messagebox, ttk

from todolist.domain.task import TaskPriority
from todolist.presentation.styles import BACKGROUND, MUTED, SURFACE


@dataclass(frozen=True, slots=True)
class TaskFormData:
    title: str
    description: str
    category: str
    priority: TaskPriority
    due_date: date | None


class TaskDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Misc,
        *,
        dialog_title: str,
        title: str = "",
        description: str = "",
        category: str = "Général",
        priority: TaskPriority = TaskPriority.NORMAL,
        due_date: date | None = None,
    ) -> None:
        super().__init__(parent)
        self.result: TaskFormData | None = None
        self.title(dialog_title)
        self.geometry("520x530")
        self.minsize(460, 480)
        self.configure(background=BACKGROUND)
        self.transient(parent)
        self.grab_set()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        card = ttk.Frame(self, style="Card.TFrame", padding=24)
        card.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        card.columnconfigure(0, weight=1)
        card.rowconfigure(7, weight=1)

        ttk.Label(card, text="Titre", background=SURFACE).grid(row=0, column=0, sticky="w")
        self._title_var = tk.StringVar(value=title)
        title_entry = ttk.Entry(card, textvariable=self._title_var)
        title_entry.grid(row=1, column=0, sticky="ew", pady=(6, 16))

        metadata = ttk.Frame(card, style="Card.TFrame")
        metadata.grid(row=2, column=0, sticky="ew", pady=(0, 16))
        metadata.columnconfigure((0, 1), weight=1)
        ttk.Label(metadata, text="Catégorie", background=SURFACE).grid(row=0, column=0, sticky="w")
        ttk.Label(metadata, text="Priorité", background=SURFACE).grid(
            row=0, column=1, sticky="w", padx=(10, 0)
        )
        self._category_var = tk.StringVar(value=category)
        self._category = ttk.Combobox(
            metadata,
            textvariable=self._category_var,
            values=("Général", "Travail", "Personnel", "Maison", "Santé", "Projet"),
        )
        self._category.grid(row=1, column=0, sticky="ew", pady=(6, 0), padx=(0, 10))
        self._priority_labels = {
            "Basse": TaskPriority.LOW,
            "Normale": TaskPriority.NORMAL,
            "Haute": TaskPriority.HIGH,
            "Urgente": TaskPriority.URGENT,
        }
        priority_label = next(
            label for label, value in self._priority_labels.items() if value == priority
        )
        self._priority_var = tk.StringVar(value=priority_label)
        ttk.Combobox(
            metadata,
            textvariable=self._priority_var,
            values=tuple(self._priority_labels),
            state="readonly",
        ).grid(row=1, column=1, sticky="ew", pady=(6, 0), padx=(10, 0))

        ttk.Label(card, text="Échéance", background=SURFACE).grid(row=3, column=0, sticky="w")
        self._due_date_var = tk.StringVar(value=due_date.isoformat() if due_date else "")
        ttk.Entry(card, textvariable=self._due_date_var).grid(
            row=4, column=0, sticky="ew", pady=(6, 3)
        )
        ttk.Label(
            card,
            text="Format AAAA-MM-JJ · laisser vide si aucune échéance",
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 8),
        ).grid(row=5, column=0, sticky="w", pady=(0, 14))

        ttk.Label(card, text="Description", background=SURFACE).grid(
            row=6, column=0, sticky="w"
        )
        self._description = tk.Text(
            card,
            height=6,
            wrap="word",
            relief="solid",
            borderwidth=1,
            background=SURFACE,
            font=("Segoe UI", 10),
            padx=8,
            pady=8,
        )
        self._description.insert("1.0", description)
        self._description.grid(row=7, column=0, sticky="nsew", pady=(6, 18))

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.grid(row=8, column=0, sticky="e")
        ttk.Button(actions, text="Annuler", command=self.destroy).pack(side="left", padx=(0, 8))
        ttk.Button(
            actions, text="Enregistrer", style="Primary.TButton", command=self._submit
        ).pack(side="left")

        self.bind("<Escape>", lambda _event: self.destroy())
        self.bind("<Control-Return>", lambda _event: self._submit())
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        title_entry.focus_set()

    def _submit(self) -> None:
        title = self._title_var.get().strip()
        if not title:
            messagebox.showerror("Titre requis", "Saisissez un titre pour la tâche.", parent=self)
            return
        raw_due_date = self._due_date_var.get().strip()
        try:
            parsed_due_date = date.fromisoformat(raw_due_date) if raw_due_date else None
        except ValueError:
            messagebox.showerror(
                "Date invalide",
                "Utilisez le format AAAA-MM-JJ, par exemple 2026-11-05.",
                parent=self,
            )
            return
        self.result = TaskFormData(
            title=title,
            description=self._description.get("1.0", "end-1c"),
            category=self._category_var.get(),
            priority=self._priority_labels[self._priority_var.get()],
            due_date=parsed_due_date,
        )
        self.destroy()


def show_task_dialog(
    parent: tk.Misc,
    *,
    dialog_title: str,
    title: str = "",
    description: str = "",
    category: str = "Général",
    priority: TaskPriority = TaskPriority.NORMAL,
    due_date: date | None = None,
) -> TaskFormData | None:
    dialog = TaskDialog(
        parent,
        dialog_title=dialog_title,
        title=title,
        description=description,
        category=category,
        priority=priority,
        due_date=due_date,
    )
    parent.wait_window(dialog)
    return dialog.result
