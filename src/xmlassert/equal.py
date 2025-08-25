from xml.etree.ElementTree import (
    canonicalize,
)

from .diffs import clean_diff


__all__ = [
    'assert_xml_equal',
]


def assert_xml_equal(actual: str, expected: str) -> None:
    """
    Securely compare XML strings with clean diff output.
    """
    if _canonical(actual) == _canonical(expected):
        return

    diff_text = clean_diff(actual, expected)
    raise AssertionError(f'XML documents differ:\n{diff_text}')


def _canonical(content: str) -> str:
    return canonicalize(
        content,
        strip_text=True,
        with_comments=False,
    )
