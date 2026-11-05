"""Fenêtre principale, navigation et composition des pages."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

import customtkinter as ctk

from todolist.domain.task import Task
from todolist.presentation.pages.dashboard_page import DashboardPage
from todolist.presentation.pages.calendar_page import CalendarPage
from todolist.presentation.pages.settings_page import SettingsPage
from todolist.presentation.pages.statistics_page import StatisticsPage
from todolist.presentation.pages.tasks_page import TasksPage
from todolist.presentation.pages.today_page import TodayPage
from todolist.presentation.responsive import LayoutMode, layout_mode
from todolist.presentation.sidebar import Sidebar
from todolist.presentation.styles import BACKGROUND, PRIMARY, PRIMARY_ACTIVE, apply_theme

if TYPE_CHECKING:
    from todolist.presentation.task_controller import TaskController


class MainWindow(tk.Tk):
    PAGE_TITLES = {
        "dashboard": ("Dashboard", "Bienvenue, voici l'essentiel de votre journée."),
        "today": ("Aujourd'hui", "Priorités et échéances à ne pas manquer."),
        "tasks": ("Mes tâches", "Organisez, recherchez et validez vos tâches."),
        "calendar": ("Calendrier", "Visualisez vos échéances dans le temps."),
        "statistics": ("Statistiques", "Visualisez votre progression en un coup d'œil."),
        "settings": ("Paramètres", "Personnalisez le comportement de l'application."),
    }

    def __init__(self) -> None:
        super().__init__()
        self._controller: TaskController | None = None
        self._layout_mode: LayoutMode | None = None
        self._current_page = "dashboard"
        self.title("Focus — Todolist")
        self.geometry("1180x720")
        self.minsize(620, 480)
        apply_theme(self)
        self._build_ui()
        self.bind("<Configure>", self._on_resize)

    def _build_ui(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._sidebar = Sidebar(self, self.show_page)
        self._sidebar.grid(row=0, column=0, sticky="nsw")

        self._content = ttk.Frame(self, style="App.TFrame", padding=(28, 22, 28, 26))
        self._content.grid(row=0, column=1, sticky="nsew")
        self._content.columnconfigure(0, weight=1)
        self._content.rowconfigure(1, weight=1)

        header = ttk.Frame(self._content, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header.columnconfigure(0, weight=1)
        self._title_label = ttk.Label(header, text="Dashboard", style="Title.TLabel")
        self._title_label.grid(row=0, column=0, sticky="w")
        self._subtitle_label = ttk.Label(
            header,
            text=self.PAGE_TITLES["dashboard"][1],
            style="Subtitle.TLabel",
        )
        self._subtitle_label.grid(row=1, column=0, sticky="w", pady=(3, 0))
        self._add_button = ctk.CTkButton(
            header,
            text="＋  Nouvelle tâche",
            height=40,
            width=150,
            corner_radius=12,
            fg_color=PRIMARY,
            bg_color=BACKGROUND,
            hover_color=PRIMARY_ACTIVE,
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self._add_task,
        )
        self._add_button.grid(row=0, column=1, rowspan=2, sticky="e")

        self._page_container = ttk.Frame(self._content, style="Page.TFrame")
        self._page_container.grid(row=1, column=0, sticky="nsew")
        self._page_container.columnconfigure(0, weight=1)
        self._page_container.rowconfigure(0, weight=1)

        self._dashboard_page = DashboardPage(self._page_container)
        self._today_page = TodayPage(self._page_container)
        self._tasks_page = TasksPage(self._page_container)
        self._calendar_page = CalendarPage(self._page_container)
        self._statistics_page = StatisticsPage(self._page_container)
        self._settings_page = SettingsPage(self._page_container)
        self._pages: dict[str, ttk.Frame] = {
            "dashboard": self._dashboard_page,
            "today": self._today_page,
            "tasks": self._tasks_page,
            "calendar": self._calendar_page,
            "statistics": self._statistics_page,
            "settings": self._settings_page,
        }
        for page in self._pages.values():
            page.grid(row=0, column=0, sticky="nsew")
        self.show_page("dashboard")

    def set_controller(self, controller: "TaskController") -> None:
        self._controller = controller
        self._tasks_page.set_controller(controller)
        self._today_page.set_controller(controller)
        self.bind("<Control-n>", lambda _event: controller.add_task())

    def show_page(self, page_name: str) -> None:
        page = self._pages.get(page_name)
        if page is None:
            return
        self._current_page = page_name
        page.tkraise()
        self._sidebar.set_active(page_name)
        title, subtitle = self.PAGE_TITLES[page_name]
        self._title_label.configure(text=title)
        self._subtitle_label.configure(text=subtitle)

    def _add_task(self) -> None:
        if self._controller is not None:
            self._controller.add_task()

    def _on_resize(self, event: tk.Event) -> None:
        if event.widget is not self:
            return
        mode = layout_mode(event.width)
        if mode == self._layout_mode:
            return
        self._layout_mode = mode
        self._sidebar.set_mode(mode)
        self._dashboard_page.set_mode(mode)
        self._today_page.set_mode(mode)
        self._tasks_page.set_mode(mode)
        self._calendar_page.set_mode(mode)
        self._statistics_page.set_mode(mode)
        self._settings_page.set_mode(mode)
        padding = 28 if mode is LayoutMode.WIDE else 18 if mode is LayoutMode.COMPACT else 12
        self._content.configure(padding=(padding, 18, padding, 20))
        self._add_button.configure(
            text="＋" if mode is LayoutMode.NARROW else "＋  Nouvelle tâche",
            width=44 if mode is LayoutMode.NARROW else 150,
        )
        if mode is LayoutMode.NARROW:
            self._subtitle_label.grid_remove()
        else:
            self._subtitle_label.grid()

    def render_tasks(self, tasks: list[Task], all_tasks: list[Task] | None = None) -> None:
        self._tasks_page.render(tasks, all_tasks)

    def render_overview(self, tasks: list[Task]) -> None:
        self._dashboard_page.render(tasks)
        self._today_page.render(tasks)
        self._calendar_page.render(tasks)
        self._statistics_page.render(tasks)
        self._settings_page.render(tasks)

    def selected_task_id(self) -> str | None:
        return self._tasks_page.selected_task_id()

    def search_text(self) -> str:
        return self._tasks_page.search_text()

    def selected_filter(self) -> str:
        return self._tasks_page.selected_filter()

    def selected_priority_filter(self) -> str:
        return self._tasks_page.selected_priority_filter()

    def auto_refresh_enabled(self) -> bool:
        return self._settings_page.auto_refresh_enabled()

    def confirm_delete(self, task_title: str) -> bool:
        return messagebox.askyesno(
            "Supprimer la tâche",
            f"Voulez-vous vraiment supprimer « {task_title} » ?",
            parent=self,
        )

    def show_error(self, message: str) -> None:
        messagebox.showerror("Une erreur est survenue", message, parent=self)

    def request_selection(self) -> None:
        messagebox.showinfo("Sélection requise", "Sélectionnez d'abord une tâche.", parent=self)
