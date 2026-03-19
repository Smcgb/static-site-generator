from enum import Enum

class TextType(Enum):
    BOLD_TEXT = 'bold'
    ITALIC_TEXT = 'italic'
    CODE_TEXT = 'code'
    ANCHOR_TEXT ='anchor'
    ALT_TEXT = 'alt'
    
class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str=None) -> None:
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url)

    def __repr__(self)-> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
