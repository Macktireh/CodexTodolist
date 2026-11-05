import pytest

from todolist.presentation.responsive import LayoutMode, layout_mode


@pytest.mark.parametrize(
    ("width", "expected"),
    [
        (1_500, LayoutMode.WIDE),
        (1_100, LayoutMode.WIDE),
        (1_099, LayoutMode.COMPACT),
        (700, LayoutMode.COMPACT),
        (699, LayoutMode.NARROW),
        (320, LayoutMode.NARROW),
    ],
)
def test_layout_mode_uses_responsive_breakpoints(width: int, expected: LayoutMode) -> None:
    assert layout_mode(width) is expected
