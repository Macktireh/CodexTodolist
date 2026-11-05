"""Composants visuels réutilisables de l'application."""

import tkinter as tk

import customtkinter as ctk

from todolist.presentation.styles import BACKGROUND, BORDER, SURFACE


class Card(ctk.CTkFrame):
    """Carte arrondie avec une vraie zone de contenu paddée."""

    def __init__(
        self,
        parent: tk.Misc,
        *,
        fill: str = SURFACE,
        background: str = BACKGROUND,
        border_color: str = BORDER,
        radius: int = 16,
        padding: tuple[int, int] = (18, 16),
    ) -> None:
        super().__init__(
            parent,
            fg_color=fill,
            bg_color=background,
            corner_radius=radius,
            border_width=1,
            border_color=border_color,
        )
        self.body = tk.Frame(self, background=fill, borderwidth=0, highlightthickness=0)
        self.body.pack(
            fill="both",
            expand=True,
            padx=padding[0],
            pady=padding[1],
        )
