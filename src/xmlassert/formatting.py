from typing import Protocol
from xml.etree.ElementTree import canonicalize

from defusedxml.ElementTree import fromstring, tostring

from .indenting import indent

__all__ = [
    'pretty_format_xml',
]


def pretty_format_xml(xml_str: str) -> str:
    """Securely format XML with clean, consistent indentation"""
    try:
        root = fromstring(xml_str)
        indent(root)
        return str(tostring(root, encoding='unicode'))
    except Exception:
        return canonicalize(xml_str, strip_text=False)
