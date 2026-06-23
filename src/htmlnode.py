
class HTMLNode():
    
    def __init__(self, tag, value, children, props= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise Exception(NotImplementedError)
    
    def props_to_html(self):
        if self.props is None or self.props == {}:
            return ""
        formatted_string = ""
        for key in self.props:
            formatted_string += f' {key.strip("")}="{self.props[key]}"'
        return formatted_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value is None:
            raise ValueError("This node has no value")
        if self.tag is None:
            return self.value
        result = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("This node has no tag")
        if self.children is None:
            raise ValueError("This node has no children")
        children_string = ""
        for child in self.children:
            children_string += child.to_html()
        result = f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"
        return result