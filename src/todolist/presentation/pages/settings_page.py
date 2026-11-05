"""Page des paramètres, du stockage et des raccourcis."""

import tkinter as tk
from tkinter import ttk

from todolist.domain.task import Task
from todolist.presentation.components import Card
from todolist.presentation.responsive import LayoutMode
from todolist.presentation.styles import BACKGROUND, BORDER, MUTED, PRIMARY, SUCCESS, SURFACE, TEXT


class SettingsPage(ttk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, style="Page.TFrame")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        status = Card(
            self,
            fill="#E7F2ED",
            background=BACKGROUND,
            border_color="#C7E4D5",
            radius=16,
            padding=(20, 16),
        )
        status.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        status_body = status.body
        status_body.columnconfigure(1, weight=1)
        tk.Label(
            status_body,
            text="✓",
            width=3,
            height=1,
            background=SUCCESS,
            foreground="white",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, rowspan=2, padx=(0, 14))
        tk.Label(
            status_body,
            text="Données locales opérationnelles",
            background="#E7F2ED",
            foreground=TEXT,
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=1, sticky="w")
        self._status_detail = tk.Label(
            status_body,
            text="Le fichier JSON est prêt.",
            background="#E7F2ED",
            foreground=MUTED,
            font=("Segoe UI", 9),
        )
        self._status_detail.grid(row=1, column=1, sticky="w", pady=(3, 0))
        tk.Label(
            status_body,
            text="VERSION 0.4.0",
            background="#E7F2ED",
            foreground=SUCCESS,
            font=("Segoe UI", 8, "bold"),
        ).grid(row=0, column=2, rowspan=2, sticky="e")

        self._sync_card = self._card("Synchronisation", "Comportement du fichier de données")
        self._sync_card.grid(row=1, column=0, sticky="nsew", padx=(0, 7))
        sync_body = self._sync_card.body
        sync_body.columnconfigure(0, weight=1)
        self._auto_refresh = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            sync_body,
            text="Actualisation automatique",
            variable=self._auto_refresh,
        ).grid(row=2, column=0, sticky="w", pady=(22, 4))
        tk.Label(
            sync_body,
            text="Relit les modifications externes toutes les deux secondes.",
            background=SURFACE,
            foreground=MUTED,
            wraplength=360,
            justify="left",
            font=("Segoe UI", 8),
        ).grid(row=3, column=0, sticky="w")
        tk.Label(
            sync_body,
            text="EMPLACEMENT DU FICHIER",
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 8, "bold"),
        ).grid(row=4, column=0, sticky="w", pady=(28, 7))
        path = ttk.Entry(sync_body)
        path.insert(0, "data/tasks.json")
        path.configure(state="readonly")
        path.grid(row=5, column=0, sticky="ew")
        tk.Label(
            sync_body,
            text="Format JSON version 1 · Écriture atomique activée",
            background=SURFACE,
            foreground=SUCCESS,
            font=("Segoe UI", 8),
        ).grid(row=6, column=0, sticky="w", pady=(9, 0))

        self._storage_card = self._card("Utilisation", "Résumé de vos données locales")
        self._storage_card.grid(row=1, column=1, sticky="nsew", padx=(7, 0))
        storage_body = self._storage_card.body
        storage_body.columnconfigure((0, 1), weight=1)
        self._total_value = self._data_metric(storage_body, 2, 0, "0", "Tâches")
        self._active_value = self._data_metric(storage_body, 2, 1, "0", "À faire")
        self._completed_value = self._data_metric(storage_body, 3, 0, "0", "Terminées")
        self._rate_value = self._data_metric(storage_body, 3, 1, "0%", "Progression")

        self._shortcuts = Card(
            self,
            fill=SURFACE,
            background=BACKGROUND,
            radius=16,
            padding=(18, 14),
        )
        self._shortcuts.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        shortcuts_body = self._shortcuts.body
        tk.Label(
            shortcuts_body,
            text="Raccourcis clavier",
            background=SURFACE,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=(0, 24))
        shortcuts = (("Ctrl + N", "Nouvelle tâche"), ("Espace", "Valider"), ("Suppr", "Supprimer"))
        for column, (keys, action) in enumerate(shortcuts, start=1):
            item = tk.Frame(shortcuts_body, background=SURFACE)
            item.grid(row=0, column=column, sticky="e", padx=12)
            tk.Label(
                item,
                text=keys,
                background="#EEECF7",
                foreground=PRIMARY,
                padx=7,
                pady=3,
                font=("Segoe UI", 8, "bold"),
            ).pack(side="left")
            tk.Label(
                item,
                text=action,
                background=SURFACE,
                foreground=MUTED,
                font=("Segoe UI", 8),
            ).pack(side="left", padx=(6, 0))

    def _card(self, title: str, subtitle: str) -> Card:
        card = Card(
            self,
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
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        tk.Label(
            body,
            text=subtitle,
            background=SURFACE,
            foreground=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(3, 0))
        return card

    @staticmethod
    def _data_metric(parent: tk.Frame, row: int, column: int, value: str, label: str) -> tk.Label:
        box = Card(
            parent,
            fill="#F7F6FB",
            background=SURFACE,
            border_color="#F7F6FB",
            radius=12,
            padding=(14, 13),
        )
        box.grid(row=row, column=column, sticky="nsew", padx=(0, 5) if column == 0 else (5, 0), pady=(18, 0))
        body = box.body
        value_label = tk.Label(
            body,
            text=value,
            background="#F7F6FB",
            foreground=TEXT,
            font=("Segoe UI", 19, "bold"),
        )
        value_label.pack(anchor="w")
        tk.Label(
            body,
            text=label,
            background="#F7F6FB",
            foreground=MUTED,
            font=("Segoe UI", 8),
        ).pack(anchor="w")
        return value_label

    def render(self, tasks: list[Task]) -> None:
        total = len(tasks)
        completed = sum(task.completed for task in tasks)
        active = total - completed
        rate = round(completed / total * 100) if total else 0
        self._status_detail.configure(text=f"{total} tâche(s) chargée(s) et synchronisée(s) localement.")
        self._total_value.configure(text=str(total))
        self._active_value.configure(text=str(active))
        self._completed_value.configure(text=str(completed))
        self._rate_value.configure(text=f"{rate}%")

    def auto_refresh_enabled(self) -> bool:
        return self._auto_refresh.get()

    def set_mode(self, mode: LayoutMode) -> None:
        if mode is LayoutMode.NARROW:
            self._sync_card.grid_configure(row=1, column=0, padx=0, pady=(0, 12))
            self._storage_card.grid_configure(row=2, column=0, padx=0)
            self._shortcuts.grid_configure(row=3, column=0, columnspan=1)
            self.columnconfigure(1, weight=0)
            self.rowconfigure(2, weight=1)
        else:
            self._sync_card.grid_configure(row=1, column=0, padx=(0, 7), pady=0)
            self._storage_card.grid_configure(row=1, column=1, padx=(7, 0))
            self._shortcuts.grid_configure(row=2, column=0, columnspan=2)
            self.columnconfigure(1, weight=1)
            self.rowconfigure(2, weight=0)
