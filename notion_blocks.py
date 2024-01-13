import re
import validators


class NotionBlock:
    """
    The JSON content to be written to the Notion page via a PATCH request
        must take the following form:

    json_content = {
        "children": [
            # block objects (JSON dicts) in this list
        ]
    }

    Block objects (in the above list) will have a unique `block_type` string
        (e.g. "heading_2") and will be of the form:

    block_object = {
        "object": "block",
        "type": block_type,
        block_type: {
            # block JSON content
        }
    }

    The block JSON content will be a dictionary of various attributes depending
        on the block type. E.g. a `rich_text` element, `color`, or `children`

    """

    block_type = None

    def __init__(self):
        # PATCH request JSON object boilerplate
        # i.e. initializes the main JSON content dictionary
        self.json_content = {
            "children": [
                # Block objects go here :)
            ]
        }

        self.block_object_attributes = {}
        self.build_block_obj_json()

    def get_json_content(self):
        return self.json_content

    def build_block_obj_json(self):
        block_object = {
            "object": "block",
            "type": self.block_type,
            self.block_type: self.block_object_attributes
        }
        self.json_content.get("children").append(block_object)

    def add_children(self, children):
        """
        Adds to the `children` block_object_attribute,
         which is of the form:
            "children": [{
                "type": child_type,
                # ... other child attributes
            }]
        :param children: list of NotionBlock objects to be added to the current block as children
        :return:
        """

        # if the current block doesn't already have a `children` attribute
        if "children" not in self.block_object_attributes.keys():
            self.block_object_attributes.update(
                {
                    "children": [{
                        "type": child.block_type,
                        child.block_type: child.block_object_attributes
                    } for child in children]
                }
            )

        # if there are already children, just extend the list
        else:
            self.block_object_attributes.get("children")[0].extend(
                [{
                    "type": child.block_type,
                    child.block_type: child.block_object_attributes
                } for child in children]
            )

    def concat_block(self, block):
        """
        :param block: a NotionBlock object to be concatenated to the overall `json_content`
            of the current block; effectively strings the blocks together
        :return:
        """
        self.json_content.get("children").append(block.json_content.get("children")[0])


class RichTextBlock(NotionBlock):
    """
    The following block types are based on display of rich text:

    Bookmark, BulletedListItem, Callout, Code, H1, H2, H3, NumberedListItem,
        Paragraph, Quote, To_Do, Toggle
    """

    def __init__(self, block_content):

        # initialize the main JSON content dictionary
        super().__init__()

        self.block_object_attributes.update(
            {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": block_content
                    }
                }]
            }
        )


notion_colors = ["blue", "brown", "default", "gray", "green", "orange", "yellow", "pink", "purple", "red",
                 "blue_background", "brown_background", "gray_background", "green_background", "orange_background",
                 "pink_background", "purple_background", "red_background", "yellow_background"]


class ColorBlock:
    def set_color(self, color: notion_colors):
        """
        :param color: - one of:
            "blue", "brown", "default", "gray", "green", "orange", "yellow", "pink", "purple", "red"
            "blue_background", "brown_background", "gray_background", "green_background", "orange_background",
                "pink_background", "purple_background", "red_background", "yellow_background"
            or see https://developers.notion.com/reference/block for the updated list
        :return:
        """
        self.block_object_attributes.update(
            {
                "color": color
            }
        )


class BookmarkBlock(NotionBlock):
    block_type = "bookmark"

    def __init__(self, url):
        super().__init__()

        self.block_object_attributes.update(
            {
                "url": url
            }
        )


class BreadcrumbBlock(NotionBlock):
    block_type = "breadcrumb"


class BulletItemBlock(RichTextBlock, ColorBlock):
    block_type = "bulleted_list_item"


class CalloutBlock(RichTextBlock, ColorBlock):
    block_type = "callout"

    def __init__(self, block_content, emoji=None):
        super().__init__(block_content)

        self.block_object_attributes.update(
            {
                "icon": {
                    "emoji": emoji if emoji is not None else "🤖"
                }
            }
        )


class CodeBlock(RichTextBlock):
    block_type = "code"

    def __init__(self, block_content, language=None):
        """
        :param block_content:
        :param language: see https://developers.notion.com/reference/block#code
            for full list of supported languages
        """
        super().__init__(block_content)

        self.block_object_attributes.update(
            {
                "language": language if language is not None else "python"
            }
        )


class ColumnsBlock(NotionBlock):
    block_type = "column_list"

    def __init__(self, columns_list):
        super().__init__()
        # TODO


class DividerBlock(NotionBlock):
    block_type = "divider"


class EmbedBlock(NotionBlock):
    block_type = "embed"

    def __init__(self, url):
        """
        From https://developers.notion.com/reference/block#embed:
        "The result is that embed blocks created via the API may not look exactly
            like their counterparts created in the Notion app."
        """
        super().__init__()

        # TODO: validate URL
        # test_url = "https://aclassictwist.com/pina-colada-ice-cream/"
        # out = validators.url(test_url)
        # if out:
        #     print("valid")

        self.block_object_attributes.update(
            {
                "url": url
            }
        )


class EquationBlock(NotionBlock):
    block_type = "equation"

    def __init__(self, block_content):
        super().__init__()

        self.block_object_attributes.update(
            {
                "expression": block_content
            }
        )


class FileBlock(NotionBlock):
    block_type = "file"

    def __init__(self, file_url, name="file"):
        super().__init__()

        self.block_object_attributes.update(
            {
                "type": "external",
                "external": {
                    "url": file_url
                },
                "name": name
            }
        )


class H1Block(RichTextBlock, ColorBlock):
    block_type = "heading_1"


class H2Block(RichTextBlock, ColorBlock):
    block_type = "heading_2"


class H3Block(RichTextBlock, ColorBlock):
    block_type = "heading_3"


class ImageBlock(NotionBlock):
    block_type = "image"

    def __init__(self, img_url):
        super().__init__()

        self.block_object_attributes.update(
            {
                "type": "external",
                "external": {
                    "url": img_url
                }
            }
        )


class MentionBlock(NotionBlock):
    block_type = "page"

    def __init__(self, page_id):
        super().__init__()

        self.block_object_attributes.update(
            {
                "id": page_id
            }
        )


class NumberedItemBlock(RichTextBlock, ColorBlock):
    block_type = "numbered_list_item"


class ParagraphBlock(RichTextBlock, ColorBlock):
    block_type = "paragraph"

    def __init__(self, block_content):
        """
        :param block_content: If greater than 2000 characters, must be broken into multiple chunks
        """
        super().__init__(block_content[:2000])

        if len(block_content) >= 2000:
            # https://medium.com/@plasmak_/how-to-create-a-notion-page-using-python-9994bf01299
            chunks = re.findall(r".{1,2000}(?=\s|$)", block_content[2000:])
            for chunk in chunks:
                self.concat_block(ParagraphBlock(chunk))


class PDFBlock(NotionBlock):
    block_type = "pdf"

    def __init__(self, pdf_url):
        super().__init__()

        self.block_object_attributes.update({
            "type": "external",
            "external": {
                "url": pdf_url
            }
        })


class QuoteBlock(RichTextBlock, ColorBlock):
    block_type = "quote"


class SyncedBlockSource(NotionBlock):
    block_type = "synced_block"

    def __init__(self, block_obj_to_sync):
        super().__init__()

        self.block_object_attributes.update(
            {
                "synced_from": None,
            }
        )
        self.add_children([block_obj_to_sync])


class SyncedBlockDuplicate(NotionBlock):
    block_type = "synced_block"

    def __init__(self, source_block_id):
        super().__init__()

        self.block_object_attributes.update(
            {
                "synced_from": {
                    "block_id": source_block_id
                }
            }
        )


class TableBlock(NotionBlock):
    block_type = "table"

    def __init__(self, width, has_col_header=True, has_row_header=False):
        super().__init__()

        # TODO
        self.block_object_attributes.update({
            "table_width": width,
            "has_column_header": has_col_header,
            "has_row_header": has_row_header,
            "children": [{}]
        })


class TableOfContentsBlock(NotionBlock, ColorBlock):
    block_type = "table_of_contents"


class ToDoBlock(RichTextBlock, ColorBlock):
    block_type = "to_do"

    def __init__(self, block_content, checked=False):
        super().__init__(block_content)

        self.block_object_attributes.update(
            {
                "checked": checked
            }
        )


class ToggleBlock(RichTextBlock, ColorBlock):
    block_type = "toggle"

    def __init__(self, block_content, children=None):
        super().__init__(block_content)

        # Add the blocks to be contained within the toggle as its children
        if children is not None:
            self.add_children(children)


class VideoBlock(NotionBlock):
    block_type = "video"

    def __init__(self, video_url):
        """
        :param video_url: See https://developers.notion.com/reference/block#video
            for full list of supported video types (including YouTube video links)
        """
        super().__init__()

        self.block_object_attributes.update(
            {
                "type": "external",
                "external": {
                    "url": video_url
                }
            }
        )
