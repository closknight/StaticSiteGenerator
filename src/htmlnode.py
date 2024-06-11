class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        if not self.props:
            return ""

        html = ""
        for key, value in self.props.items():
            html += f" {key}=\"{value}\""

        return html
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError()
        if self.tag is None:
            return self.value
        return (
            f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        )
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode has no tag")
        if self.children is None:
            raise ValueError("ParentNode has no children")
        children = ""
        for child in self.children:
            children += child.to_html()

        return f"<{self.tag}>{children}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    