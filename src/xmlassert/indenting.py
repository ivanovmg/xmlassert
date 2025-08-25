from __future__ import annotations

from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from xml.etree.ElementTree import Element

__all__ = [
    'indent',
]


def indent(elem: Element, level: int = 0) -> None:
    """
    Recursively indent XML elements with consistent spacing.
    Based on the standard ElementTree indentation approach.
    """
    # Set indentation for current element
    indent_str = '\n' + '  ' * level

    if len(elem):
        # If element has children
        if not elem.text or not elem.text.strip():
            elem.text = indent_str + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent_str

        # Process children
        for child in elem:
            indent(child, level + 1)

        # Set tail for the last child
        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = indent_str

    else:
        # Leaf element
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent_str
