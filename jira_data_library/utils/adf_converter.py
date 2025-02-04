"""
Converts an Atlassian Document Format (ADF) structure into a markdown-like string.
"""

class ADFConverter:
    """
    The ADFConverter class provides static methods to validate and convert ADF nodes
    into a markdown-like representation. It handles various ADF node types such as
    documents, text, paragraphs, headings, lists, tables, and more. The conversion
    process also tracks unsupported node types and marks, adding them to a warnings
    set for further handling if necessary.

    Methods:
        convert(adf): Validates and converts the given ADF structure, returning the
            result and any warnings encountered.
        validate(adf): Performs basic validation on the ADF structure.
        _convert(node, warnings, order=None): Recursively converts ADF nodes to a
            markdown-like format, updating warnings for unsupported types.
        _convert_marks(node, warnings): Converts text node marks to markdown-like
            syntax, updating warnings for unsupported marks.
    """

    MEDIA_HOST = "https://your-media-host"

    @staticmethod
    def convert(adf):
        """
        Validates and converts the given ADF structure into a markdown-like format.

        This method first validates the ADF structure to ensure it meets basic
        requirements. It then converts the ADF into a markdown-like string,
        collecting any warnings about unsupported node types or marks during
        the conversion process.

        Args:
            adf (dict): The ADF structure to be converted.

        Returns:
            dict: A dictionary containing the conversion result as a string
            under the key "result", and a set of warnings under the key "warnings".
        """
        warnings = set()
        ADFConverter.validate(adf)
        result = ADFConverter._convert(adf, warnings)
        return {
            "result": result,
            "warnings": warnings
        }

    @staticmethod
    def validate(adf):
        """
        Validates the given ADF structure to ensure it is a valid document.

        This method checks if the provided ADF is a dictionary with a "type"
        of "doc" and a "version" of 1. If these conditions are not met, a
        ValueError is raised.

        Args:
            adf (dict): The ADF structure to be validated.

        Raises:
            ValueError: If the ADF structure is not valid.
        """
        if not isinstance(adf, dict) or adf.get("type") != "doc" or adf.get("version") != 1:
            raise ValueError("adf-validation-failed")

    @staticmethod
    def _convert(node, warnings, order=None):
        """
        Recursively converts an ADF node into a markdown-like string.

        This static method processes various ADF node types, converting them
        into a markdown-like format. It handles nodes such as documents, text,
        paragraphs, headings, lists, tables, and more. Unsupported node types
        are added to the warnings set for further handling.

        Args:
            node (dict): The ADF node to be converted.
            warnings (set): A set to collect unsupported node types.
            order (int, optional): The starting order number for ordered lists.

        Returns:
            str: The markdown-like representation of the ADF node.
        """
        content = node.get("content", [])

        match node["type"]:
            case "doc":
                return "\n\n".join(ADFConverter._convert(child, warnings) for child in content)

            case "text":
                return ADFConverter._convert_marks(node, warnings)

            case "paragraph":
                return "".join(ADFConverter._convert(child, warnings) for child in content)

            case "heading":
                level = node.get("attrs", {}).get("level", 1)
                heading = "#" * level
                return f"{heading} {''.join(ADFConverter._convert(child, warnings) for
                                            child in content)}"

            case "hardBreak":
                return "\n"

            case "inlineCard" | "blockCard" | "embedCard":
                url = node.get("attrs", {}).get("url", "")
                return f"[{url}]({url})"

            case "blockquote":
                blockquote = "\n> ".join(ADFConverter._convert(child, warnings) for
                                         child in content)
                return f"> {blockquote}"

            case "bulletList":
                return "\n".join(ADFConverter._convert(child, warnings) for child in content)

            case "orderedList":
                order = node.get("attrs", {}).get("order", 1)
                converted = []
                for child in content:
                    converted.append(ADFConverter._convert(child, warnings, order))
                    order += 1
                return "\n".join(converted)

            case "listItem":
                is_ordered = isinstance(order, int)
                symbol = f"{order}." if is_ordered else "*"
                return f"  {symbol} {''.join(ADFConverter._convert(child, warnings).rstrip()
                                             for child in content)}"

            case "codeBlock":
                language = node.get("attrs", {}).get("language", "")
                code = "\n".join(ADFConverter._convert(child, warnings) for child in content)
                return f"```{language}\n{code}\n```"

            case "rule":
                return "\n\n---\n"

            case "emoji":
                return node.get("attrs", {}).get("shortName", "")

            case "table":
                return "\n".join(ADFConverter._convert(child, warnings) for child in content)

            case "tableRow":
                th_count = 0
                output = "|"
                for sub_node in content:
                    if sub_node["type"] == "tableHeader":
                        th_count += 1
                    output += ADFConverter._convert(sub_node, warnings)
                if th_count:
                    output += f"\n{'|:-:' * th_count}|\n"
                return output

            case "tableHeader" | "tableCell":
                return "".join(ADFConverter._convert(child, warnings) for child in content) + "|"

            case "mediaSingle":
                if content and content[0]["type"] == "media":
                    media_node = content[0]
                    media_attrs = media_node.get("attrs", {})
                    alt_text = media_attrs.get("alt", "Media")
                    return f"![{alt_text}]({ADFConverter.MEDIA_HOST}/{media_attrs.get('id')})"
                return ""

            case "mediaInline":
                media_attrs = node.get("attrs", {})
                media_id = media_attrs.get("id")
                return f"[Media]({ADFConverter.MEDIA_HOST}/{media_id})" if media_id else ""

            case _:
                warnings.add(node["type"])
                return ""

    @staticmethod
    def _convert_marks(node, warnings):
        """
        Converts text node marks to markdown-like syntax.

        This static method processes the 'marks' attribute of a text node,
        applying markdown-like formatting based on the type of mark. Supported
        marks include 'code', 'em', 'link', 'strike', and 'strong'. Unsupported
        marks are added to the warnings set for further handling.

        Args:
            node (dict): The text node containing 'text' and 'marks' attributes.
            warnings (set): A set to collect unsupported mark types.

        Returns:
            str: The text with applied markdown-like formatting.
        """
        if not isinstance(node.get("marks"), list):
            return node.get("text", "")

        text = node["text"]
        for mark in node["marks"]:
            match mark["type"]:
                case "code":
                    text = f"`{text}`"
                case "em":
                    text = f"_{text}_"
                case "link":
                    href = mark.get("attrs", {}).get("href", "")
                    text = f"[{text}]({href})"
                case "strike":
                    text = f"~~{text}~~"
                case "strong":
                    text = f"**{text}**"
                case _:
                    warnings.add(mark["type"])
        return text
