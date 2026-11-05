"""Exceptions propres à l'application."""


class TodolistError(Exception):
    """Erreur de base présentable à l'utilisateur."""


class TaskValidationError(TodolistError):
    """Les informations d'une tâche ne sont pas valides."""


class TaskNotFoundError(TodolistError):
    """La tâche demandée n'existe pas."""


class StorageError(TodolistError):
    """Les tâches n'ont pas pu être lues ou enregistrées."""
