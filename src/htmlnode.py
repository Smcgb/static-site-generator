from enum import Enum

class HTMLNode:
    def __init__(self, 
                 tag: str | None=None, 
                 value: str | None=None, 
                 children: list[object] | None =None, 
                 props: dict | None=None)-> None:

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:

        rep_str = ''

        if self.props:
            for k,v in self.props.items():
                rep_str += f'{k}="{v}" '

        return rep_str

    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return NotImplemented

        return (self.tag, self.value, self.children, self.props) == (other.tag, other.value, other.children, other.props)


class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None):
        if not value:
            raise ValueError("Value is required.")
        super().__init__(value=value, tag=tag, props=props)

        self.children = None

    def to_html(self):
        if self.tag in [None, ""]:
            return self.value
        
        if self.props != None:

            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.props})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return NotImplemented

        return (self.tag, self.value,  self.props) == (other.tag, other.value, other.props)
