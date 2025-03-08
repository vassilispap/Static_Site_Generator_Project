import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):

    prop1 = {
    "href": "https://www.google.com",
    "target": "_blank",
}
    prop2 = {
    "href": "https://www.boot.dev",
    "target": "_bl",
}
    prop3 = {
    "href": "https://www.google.com",
    "target": "_blank",
}

    def test_repr1(self):
        node = HTMLNode(None, None, None, self.prop1)
        print(node.props)
        
    def test_repr2(self):
        node = HTMLNode(None, None, None, self.prop2)
        print(node.props)
        
    def test_repr3(self):
        node = HTMLNode(None, None, None, self.prop3)
        print(node.props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        

if __name__ == "__main__":
    unittest.main()
