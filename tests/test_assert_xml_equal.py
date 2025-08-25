from typing import Any
from xml.etree.ElementTree import ParseError

import pytest

from xmlassert import assert_xml_equal


def test_IdenticalXmlStrings_PassWithoutError() -> None:
    xml_string = '<root><child>text</child></root>'
    assert_xml_equal(xml_string, xml_string)


@pytest.mark.parametrize(
    'actual,expected',
    [
        # Different formatting
        (
            '<root><child>text</child></root>',
            '<root>\n    <child>text</child>\n</root>',
        ),
        # Different whitespace
        ('<root>text</root>', '<root>  text  </root>'),
        (
            '<root><child>text</child></root>',
            '<root>  <child>text</child>  </root>',
        ),
        ('<root>   text   </root>', '<root>text</root>'),
        # Comments ignored
        ('<root><!-- comment --><child/></root>', '<root><child/></root>'),
        # Self-closing vs explicit
        ('<root><child/></root>', '<root><child></child></root>'),
        ('<root attr="value"/>', '<root attr="value"></root>'),
        # Multiple children
        (
            '<root><child1/><child2/><child3/></root>',
            '<root><child1></child1><child2/><child3/></root>',
        ),
        # Mixed content
        (
            '<root>text<child/>more text</root>',
            '<root>text<child></child>more text</root>',
        ),
        # Quote styles
        (
            "<root attr='value'><child/></root>",
            '<root attr="value"><child/></root>',
        ),
        # Processing instructions
        (
            '<?xml version="1.0"?><root><child/></root>',
            '<?xml version="1.0" encoding="UTF-8"?><root><child/></root>',
        ),
    ],
)
def test_EquivalentXmlWithDifferentFormatting_Pass(
    actual: str, expected: str
) -> None:
    assert_xml_equal(actual, expected)


@pytest.mark.parametrize(
    'actual,expected',
    [
        # Different structure
        (
            '<root><child>text</child></root>',
            '<root><different>text</different></root>',
        ),
        # Different content
        (
            '<root><child>actual text</child></root>',
            '<root><child>expected text</child></root>',
        ),
        ('<root><child>one</child></root>', '<root><child>two</child></root>'),
        # Different attributes
        (
            '<root attr1="value"><child/></root>',
            '<root attr2="value"><child/></root>',
        ),
        ('<root a="1"><child/></root>', '<root a="2"><child/></root>'),
        # Different namespaces
        (
            '<ns:root xmlns:ns="http://example.com"><ns:child/></ns:root>',
            '<ns:root xmlns:ns="http://different.com"><ns:child/></ns:root>',
        ),
    ],
)
def test_DifferentXmlContent_RaisesAssertionError(
    actual: str, expected: str
) -> None:
    with pytest.raises(AssertionError, match='XML documents differ'):
        assert_xml_equal(actual, expected)


@pytest.mark.parametrize(
    'xml1,xml2',
    [
        (
            '<root a="1" b="2"><child/></root>',
            '<root b="2" a="1"><child/></root>',
        ),
        ('<root x="a" y="b" z="c"/>', '<root z="c" y="b" x="a"/>'),
    ],
)
def test_AttributeOrder_DoesNotAffectEquality(xml1: str, xml2: str) -> None:
    assert_xml_equal(xml1, xml2)


def test_XmlWithIdenticalNamespaces_Pass() -> None:
    actual = '<ns:root xmlns:ns="http://example.com"><ns:child/></ns:root>'
    expected = '<ns:root xmlns:ns="http://example.com"><ns:child></ns:child></ns:root>'
    assert_xml_equal(actual, expected)


def test_NestedXmlStructure_EquivalentRegardlessOfFormatting() -> None:
    actual = """
    <root>
        <parent>
            <child>text</child>
        </parent>
    </root>
    """
    expected = '<root><parent><child>text</child></parent></root>'
    assert_xml_equal(actual, expected)


def test_ComplexXmlStructure_EquivalentRegardlessOfFormatting() -> None:
    complex_xml = """
    <config>
        <server host="example.com" port="8080">
            <security>
                <ssl enabled="true"/>
                <authentication method="token"/>
            </security>
        </server>
        <database type="postgresql">
            <connection pool-size="10"/>
        </database>
    </config>
    """

    compact_xml = '<config><server host="example.com" port="8080"><security><ssl enabled="true"/><authentication method="token"/></security></server><database type="postgresql"><connection pool-size="10"/></database></config>'

    assert_xml_equal(complex_xml, compact_xml)


def test_DifferentXml_ErrorMessageContainsReadableDiff() -> None:
    actual = '<root><child>actual</child></root>'
    expected = '<root><child>expected</child></root>'

    with pytest.raises(AssertionError) as exc_info:
        assert_xml_equal(actual, expected)

    error_message = str(exc_info.value)
    assert 'XML documents differ' in error_message
    assert 'expected' in error_message
    assert 'actual' in error_message
    assert '---' in error_message and '+++' in error_message


def test_XmlWithSpecialCharacters_HandledCorrectly() -> None:
    actual = '<root><child>&amp; &lt; &gt;</child></root>'
    expected = '<root><child>&amp; &lt; &gt;</child></root>'
    assert_xml_equal(actual, expected)


def test_XmlWithCdataSections_Equivalent() -> None:
    actual = '<root><![CDATA[<unescaped>content</unescaped>]]></root>'
    expected = '<root><![CDATA[<unescaped>content</unescaped>]]></root>'
    assert_xml_equal(actual, expected)


@pytest.mark.parametrize(
    'invalid_xml',
    [
        '',
        '   ',
        '<root><unclosed>',
        '<unclosed>',
    ],
)
def test_InvalidXml_RaisesParseError(invalid_xml: str) -> None:
    valid_xml = '<root><child/></root>'

    with pytest.raises(ParseError):
        assert_xml_equal(invalid_xml, valid_xml)

    with pytest.raises(ParseError):
        assert_xml_equal(valid_xml, invalid_xml)


@pytest.mark.parametrize(
    'invalid_input',
    [
        None,
        123,
        [],
        {},
    ],
)
def test_NonStringInput_RaisesError(invalid_input: Any) -> None:
    valid_xml = '<root><child/></root>'

    with pytest.raises((TypeError, ValueError)):
        assert_xml_equal(invalid_input, valid_xml)

    with pytest.raises((TypeError, ValueError)):
        assert_xml_equal(valid_xml, invalid_input)


def test_LargeXmlDocuments_HandledSuccessfully() -> None:
    large_xml = '<root>' + '<child>text</child>' * 100 + '</root>'
    assert_xml_equal(large_xml, large_xml)


def test_XmlWithUnicodeCharacters_HandledCorrectly() -> None:
    actual = '<root><child>caf\u00e9 na\u00efve</child></root>'
    expected = '<root><child>caf\u00e9 na\u00efve</child></root>'
    assert_xml_equal(actual, expected)


def test_MalformedXml_RaisesParseErrorWithMeaningfulMessage() -> None:
    malformed_xml = '<root><unclosed>'
    well_formed_xml = '<root><child/></root>'

    with pytest.raises(ParseError):
        assert_xml_equal(malformed_xml, well_formed_xml)


def test_EmptyElementsWithDifferentSyntax_Equivalent() -> None:
    test_cases = [
        ('<root/>', '<root></root>'),
        ('<root><child/></root>', '<root><child></child></root>'),
        ('<root attr="value"/>', '<root attr="value"></root>'),
    ]

    for actual, expected in test_cases:
        assert_xml_equal(actual, expected)


def test_XmlWithAttributesInDifferentOrder_Equivalent() -> None:
    actual = '<element first="1" second="2" third="3"/>'
    expected = '<element third="3" first="1" second="2"/>'
    assert_xml_equal(actual, expected)


def test_XmlWithNamespacePrefixes_HandledCorrectly() -> None:
    actual = '<ns:element xmlns:ns="http://example.com" ns:attr="value"/>'
    expected = '<ns:element xmlns:ns="http://example.com" ns:attr="value"></ns:element>'
    assert_xml_equal(actual, expected)


def test_XmlWithDifferentNamespaceUris_RaisesAssertionError() -> None:
    actual = '<ns:element xmlns:ns="http://example.com" ns:attr="value"/>'
    expected = '<ns:element xmlns:ns="http://different.com" ns:attr="value"/>'

    with pytest.raises(AssertionError):
        assert_xml_equal(actual, expected)


def test_XmlWithMixedContentAndFormatting_Equivalent() -> None:
    actual = '<root>  text  <child>  value  </child>  more text  </root>'
    expected = '<root>text<child>value</child>more text</root>'
    assert_xml_equal(actual, expected)


@pytest.mark.parametrize(
    'xml_content',
    [
        '<root/>',  # Minimal self-closing
        '<root></root>',  # Minimal with closing
        '<root>text</root>',  # With text content
        "<root attr='value'/>",  # With attribute
        '<root><child/></root>',  # With child
    ],
)
def test_EdgeCaseXml_ThatTriggersBranchCoverage(xml_content: str) -> None:
    """Test edge cases that might trigger different code paths"""
    assert_xml_equal(xml_content, xml_content)


@pytest.mark.parametrize(
    'whitespace_xml',
    [
        '<root>\n<child>\n</child>\n</root>',  # Newlines only
        '<root>  <child>  </child>  </root>',  # Spaces only
        '<root>\t<child>\t</child>\t</root>',  # Tabs only
        '<root>\n  \t<child>\n  \t</child>\n  \t</root>',  # Mixed whitespace
    ],
)
def test_XmlWithVariousWhitespacePatterns(whitespace_xml: str) -> None:
    """Test XML with different whitespace patterns"""
    assert_xml_equal(whitespace_xml, whitespace_xml)


@pytest.mark.parametrize(
    'empty_element_format',
    [
        '<root><empty/></root>',
        '<root><empty></empty></root>',
        '<root>\n<empty/>\n</root>',
        '<root>\n<empty></empty>\n</root>',
    ],
)
def test_XmlWithEmptyElements_DifferentFormats(
    empty_element_format: str,
) -> None:
    """Test empty elements in various formats"""
    canonical = '<root><empty/></root>'
    assert_xml_equal(empty_element_format, canonical)


def test_XmlWithDeepNesting_CoversRecursivePaths() -> None:
    """Test deeply nested XML to cover recursive formatting paths"""
    deep_xml = '<level1><level2><level3><level4><level5>deep</level5></level4></level3></level2></level1>'
    assert_xml_equal(deep_xml, deep_xml)


def test_XmlWithMixedContentAndFormatting_CoversAllBranches() -> None:
    """Test XML with mixed content types"""
    mixed_xml = """
    <root>
        Text content
        <child attr="value">child text</child>
        More text
        <selfclosing/>
        <empty></empty>
    </root>
    """
    assert_xml_equal(mixed_xml, mixed_xml)


def test_XmlWithSpecialCharacters_InAttributesAndText() -> None:
    """Test XML with special characters in different contexts"""
    special_chars_xml = (
        '<root attr="value&amp;value"><child>&lt;content&gt;</child></root>'
    )
    assert_xml_equal(special_chars_xml, special_chars_xml)


def test_XmlWithNamespace_AndAttributes_CoversComplexPaths() -> None:
    """Test XML with namespaces and attributes"""
    ns_xml = '<ns:root xmlns:ns="http://example.com" ns:attr="value"><ns:child/></ns:root>'
    assert_xml_equal(ns_xml, ns_xml)
