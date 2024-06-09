from htmlnode import HTMLNode


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