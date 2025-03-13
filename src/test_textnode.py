import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node3)
    
    def test_eq3(self):
        node10 = TextNode("tria poulakia kathontan", TextType.ITALIC, "www.google.com")
        node11 = TextNode("tria poulakia kathontan", TextType.ITALIC, "www.boot.dev")
        self.assertNotEqual(node10, node11)


if __name__ == "__main__":
    unittest.main()
