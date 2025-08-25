import difflib

from .formatting import pretty_format_xml


__all__ = [
    'clean_diff',
]


def clean_diff(actual: str, expected: str) -> str:
    actual_pretty = pretty_format_xml(actual)
    expected_pretty = pretty_format_xml(expected)
    diff = difflib.unified_diff(
        expected_pretty.splitlines(),
        actual_pretty.splitlines(),
        fromfile='expected',
        tofile='actual',
        lineterm='',
    )
    return '\n'.join(diff)
