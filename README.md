# xmlassert

**xmlassert** is a Python library designed for comparing XML documents in tests,
providing clean,
human-readable diffs when assertions fail.
Unlike raw XML comparison tools,
it ignores formatting differences and focuses on semantic equivalence.

## Features

- **Human-readable diffs**: Get clean, formatted diff output instead of cryptic XML comparisons
- **Formatting-agnostic**: Ignores whitespace, indentation, and formatting variations
- **Secure parsing**: Uses secure XML parsing practices by default
- **Test-friendly**: Perfect for `pytest`, `unittest`, and other testing frameworks

## Installation

```bash
pip install xmlassert
```

## Quick Start

``` python
from xmlassert import assert_xml_equal

# These will pass (formatting differences are ignored)
assert_xml_equal("<root><a>text</a></root>", "<root>\n  <a>text</a>\n</root>")

# This will fail with a clean diff
try:
    assert_xml_equal(
        "<root><a>expected</a></root>",
        "<root><a>actual</a></root>"
    )
except AssertionError as e:
    print(e)  # Shows beautiful diff output
```


## Usage Examples

### Basic XML Comparison

``` python
from xmlassert import assert_xml_equal

# Passes - formatting differences are ignored
xml1 = "<root><element>value</element></root>"
xml2 = """
<root>
    <element>value</element>
</root>
"""
assert_xml_equal(xml1, xml2)
```


### Pytest Example

``` python
import pytest
from xmlassert import assert_xml_equal

def test_xml_generation():
    generated_xml = generate_xml()  # Your function
    expected_xml = """
    <config>
        <setting enabled="true">value</setting>
    </config>
    """
    assert_xml_equal(generated_xml, expected_xml)
```


### Handling XML with Comments

``` python
from xmlassert import assert_xml_equal

# Comments are ignored by default in comparison
xml_with_comments = """
<root>
    <!-- This comment is ignored -->
    <element>value</element>
</root>
"""
xml_without_comments = "<root><element>value</element></root>"
assert_xml_equal(xml_with_comments, xml_without_comments)  # Passes
```

### Sample Output

When comparison fails, you get clean, readable diffs:

``` diff
AssertionError: XML documents differ:
--- expected
+++ actual
@@ -1,3 +1,3 @@
 <root>
-  <element>expected value</element>
+  <element>actual value</element>
 </root>
```

Instead of the unreadable:
```
AssertionError: XML mismatch: <root><element>expected value</element></root> != <root><element>actual value</element></root>
```
