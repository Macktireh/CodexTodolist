"""Barre de navigation latérale de l'application."""

import tkinter as tk
from collections.abc import Callable

import customtkinter as ctk

from todolist.presentation.responsive import LayoutMode
from todolist.presentation.styles import (
    SIDEBAR,
    SIDEBAR_ACTIVE,
    SIDEBAR_MUTED,
)


class Sidebar(tk.Frame):
    ITEMS = (
        ("dashboard", "⌂", "Dashboard"),
        ("today", "☀", "Aujourd'hui"),
        ("tasks", "✓", "Mes tâches"),
        ("calendar", "▦", "Calendrier"),
        ("statistics", "▥", "Statistiques"),
        ("settings", "⚙", "Paramètres"),
    )

    def __init__(self, parent: tk.Misc, on_navigate: Callable[[str], None]) -> None:
        super().__init__(parent, background=SIDEBAR, width=230)
        self.grid_propagate(False)
        self._on_navigate = on_navigate
        self._active_page = "dashboard"
        self._mode = LayoutMode.WIDE
        self._buttons: dict[str, ctk.CTkButton] = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self._brand = tk.Label(
            self,
            text="  ◈  Focus",
            anchor="w",
            background=SIDEBAR,
            foreground="white",
            font=("Segoe UI", 17, "bold"),
        )
        self._brand.grid(row=0, column=0, sticky="ew", padx=18, pady=(25, 34))

        navigation = tk.Frame(self, background=SIDEBAR)
        navigation.grid(row=1, column=0, sticky="new", padx=12)
        navigation.columnconfigure(0, weight=1)

        for row, (page, icon, label) in enumerate(self.ITEMS):
            button = ctk.CTkButton(
                navigation,
                text=f"{icon}   {label}",
                anchor="w",
                height=44,
                corner_radius=14,
                border_width=0,
                fg_color="transparent",
                bg_color=SIDEBAR,
                hover_color=SIDEBAR_ACTIVE,
                text_color=SIDEBAR_MUTED,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                cursor="hand2",
                command=lambda selected=page: self._select(selected),
            )
            button.grid(row=row, column=0, sticky="ew", pady=3)
            self._buttons[page] = button

        self._footer = tk.Label(
            self,
            text="FOCUS · TODOLIST\nPython 3.14",
            justify="left",
            anchor="w",
            background=SIDEBAR,
            foreground=SIDEBAR_MUTED,
            font=("Segoe UI", 8),
        )
        self._footer.grid(row=3, column=0, sticky="sew", padx=26, pady=22)
        self.set_active("dashboard")

    def _select(self, page: str) -> None:
        self.set_active(page)
        self._on_navigate(page)

    def set_active(self, page: str) -> None:
        self._active_page = page
        for name, button in self._buttons.items():
            active = name == page
            button.configure(
                fg_color=SIDEBAR_ACTIVE if active else "transparent",
                text_color="white" if active else SIDEBAR_MUTED,
            )

    def set_mode(self, mode: LayoutMode) -> None:
        if mode == self._mode:
            return
        self._mode = mode
        compact = mode is not LayoutMode.WIDE
        self.configure(width=72 if compact else 230)
        self._brand.configure(text="◈" if compact else "  ◈  Focus", anchor="center" if compact else "w")
        self._brand.grid_configure(padx=8 if compact else 18)
        self._footer.configure(text="3.14" if compact else "FOCUS · TODOLIST\nPython 3.14", anchor="center" if compact else "w")
        self._footer.grid_configure(padx=8 if compact else 26)
        for page, icon, label in self.ITEMS:
            self._buttons[page].configure(
                text=icon if compact else f"{icon}   {label}",
                anchor="center" if compact else "w",
            )
