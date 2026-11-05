"""Thème visuel de l'application."""

import tkinter as tk
from tkinter import font, ttk

BACKGROUND = "#F4F7FB"
SURFACE = "#FFFFFF"
TEXT = "#172033"
MUTED = "#667085"
PRIMARY = "#6757D9"
PRIMARY_ACTIVE = "#5546C5"
DANGER = "#C43D4B"
BORDER = "#DDE3EC"
SUCCESS = "#20845B"
SIDEBAR = "#17152B"
SIDEBAR_ACTIVE = "#302B55"
SIDEBAR_MUTED = "#AAA5C4"


def apply_theme(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")

    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Segoe UI", size=10)
    font.nametofont("TkTextFont").configure(family="Segoe UI", size=10)

    root.configure(background=BACKGROUND)
    style.configure("App.TFrame", background=BACKGROUND)
    style.configure("Page.TFrame", background=BACKGROUND)
    style.configure("Card.TFrame", background=SURFACE)
    style.configure("TLabel", background=BACKGROUND, foreground=TEXT)
    style.configure("Muted.TLabel", background=BACKGROUND, foreground=MUTED)
    style.configure(
        "Title.TLabel", background=BACKGROUND, foreground=TEXT, font=("Segoe UI", 22, "bold")
    )
    style.configure("Subtitle.TLabel", background=BACKGROUND, foreground=MUTED)
    style.configure(
        "Count.TLabel", background=SURFACE, foreground=MUTED, font=("Segoe UI", 9)
    )
    style.configure(
        "Primary.TButton",
        background=PRIMARY,
        foreground="white",
        borderwidth=0,
        padding=(16, 9),
        font=("Segoe UI", 10, "bold"),
    )
    style.map("Primary.TButton", background=[("active", PRIMARY_ACTIVE)])
    style.configure("Secondary.TButton", padding=(12, 8))
    style.configure("Danger.TButton", foreground=DANGER, padding=(12, 8))
    style.configure(
        "Tasks.Treeview",
        background=SURFACE,
        fieldbackground=SURFACE,
        foreground=TEXT,
        rowheight=42,
        borderwidth=0,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Tasks.Treeview.Heading",
        background="#EEF1F6",
        foreground=MUTED,
        relief="flat",
        padding=(8, 8),
        font=("Segoe UI", 9, "bold"),
    )
    style.map(
        "Tasks.Treeview",
        background=[("selected", "#E8E4FF")],
        foreground=[("selected", TEXT)],
    )
    style.configure("TEntry", padding=8, fieldbackground=SURFACE)
    style.configure("TCombobox", padding=7, fieldbackground=SURFACE)
    style.configure(
        "Accent.Horizontal.TProgressbar",
        background=PRIMARY,
        troughcolor="#E8E5F5",
        borderwidth=0,
        thickness=10,
    )
    style.configure(
        "Success.Horizontal.TProgressbar",
        background=SUCCESS,
        troughcolor="#E7F2ED",
        borderwidth=0,
        thickness=10,
    )
    style.configure(
        "Warning.Horizontal.TProgressbar",
        background="#E78B39",
        troughcolor="#FAEDE2",
        borderwidth=0,
        thickness=10,
    )
