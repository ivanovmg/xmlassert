from typing import Protocol
from xml.etree.ElementTree import (
    Element,  # For type hints only
    canonicalize,
)

from defusedxml.ElementTree import fromstring, tostring


__all__ = [
    'pretty_format_xml',
]


def pretty_format_xml(xml_str: str) -> str:
    """Securely format XML with clean, consistent indentation"""
    try:
        root = fromstring(xml_str)
        _indent(root)
        return str(tostring(root, encoding='unicode'))
    except Exception:
        return canonicalize(xml_str, strip_text=False)


class ElementVisitor(Protocol):
    def visit(self, elem: Element, level: int) -> None: ...


class IndentVisitorFactory:
    """Factory that provides appropriate visitors based on element type"""

    @staticmethod
    def get_pre_visitor(elem: Element) -> ElementVisitor:
        if len(elem):
            return ParentElementVisitor()
        return LeafElementVisitor()

    @staticmethod
    def get_post_visitor(elem: Element) -> ElementVisitor:
        return PostProcessingVisitor()


class ParentElementVisitor:
    def visit(self, elem: Element, level: int) -> None:
        indent_str = '  ' * level
        if not elem.text or not elem.text.strip():
            elem.text = '\n' + indent_str + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = '\n' + indent_str


class LeafElementVisitor:
    def visit(self, elem: Element, level: int) -> None:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = '\n' + '  ' * level


class PostProcessingVisitor:
    def visit(self, elem: Element, level: int) -> None:
        if len(elem) and (not elem.tail or not elem.tail.strip()):
            elem.tail = '\n' + '  ' * level


def _indent(elem: Element, level: int = 0) -> None:
    """Recursively indent XML elements using visitor factory"""
    factory = IndentVisitorFactory()
    _traverse_with_factory(elem, factory, level)


def _traverse_with_factory(
    elem: Element, factory: IndentVisitorFactory, level: int = 0
) -> None:
    # Pre-visit with appropriate visitor
    pre_visitor = factory.get_pre_visitor(elem)
    pre_visitor.visit(elem, level)

    # Process children
    for child in elem:
        _traverse_with_factory(child, factory, level + 1)

    # Post-visit
    post_visitor = factory.get_post_visitor(elem)
    post_visitor.visit(elem, level)
