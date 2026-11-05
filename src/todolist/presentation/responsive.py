"""Règles de mise en page adaptative partagées par l'interface."""

from enum import StrEnum


class LayoutMode(StrEnum):
    WIDE = "wide"
    COMPACT = "compact"
    NARROW = "narrow"


def layout_mode(width: int) -> LayoutMode:
    if width >= 1_100:
        return LayoutMode.WIDE
    if width >= 700:
        return LayoutMode.COMPACT
    return LayoutMode.NARROW
