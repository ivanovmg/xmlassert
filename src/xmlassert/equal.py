from .diffs import clean_diff
from .formatting import canonical


__all__ = [
    'assert_xml_equal',
]


def assert_xml_equal(actual: str, expected: str) -> None:
    """
    Securely compare XML strings with clean diff output.
    """
    if canonical(actual) == canonical(expected):
        return

    diff_text = clean_diff(actual, expected)
    raise AssertionError(f'XML documents differ:\n{diff_text}')
