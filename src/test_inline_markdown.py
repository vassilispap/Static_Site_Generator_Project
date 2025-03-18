import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is text with an image"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images3(self):
        matches = extract_markdown_images("![alt](https://example.com/image.png) and [a link](https://example.com).")
        self.assertListEqual([("alt", "https://example.com/image.png")], matches)


#print(extract_markdown_images(text))
#print(extract_markdown_links(text))


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "[link](https://boot.dev), that's a link and that's another one [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_extract_markdown_links3(self):
        matches = extract_markdown_links(
            "![alt](https://example.com/image.png) and [a link](https://example.com)."
        )
        self.assertListEqual([("a link", "https://example.com")], matches)

    def test_split_nodes_image(self):
        nodes = [
            TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,)]
        list1 = split_nodes_image(nodes)
        self.assertListEqual(split_nodes_image(nodes), 
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ]
        )

    def test_split_nodes_link(self):
        nodes = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,)]
        self.assertListEqual(split_nodes_link(nodes), 
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ]
        )

    def test_basic_image(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_multiple_images(self):
        node = TextNode(
            "![first](https://example.com/first.png) and ![second](https://example.com/second.png)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://example.com/first.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "https://example.com/second.png"),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode("Text followed by ![end](https://example.com/end.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode("![start](https://example.com/start.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_basic_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )


    def test_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        test_node = text_to_textnodes(node)
        self.assertListEqual(text_to_textnodes(node), [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ])
    
    def test_text_to_textnodes2(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        test_node = text_to_textnodes(node)
        self.assertListEqual(text_to_textnodes(node), [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_text_to_textnodes3(self):
        node = TextNode("This is just a text", TextType.TEXT)
        test_node = text_to_textnodes(node)
        self.assertListEqual(text_to_textnodes(node), [
        TextNode("This is just a text", TextType.TEXT),
        ])

    def test_text_to_textnodes4(self):
        node = TextNode("![image](https://example.com/image.jpg) is a picture and a [link](https://example.com) goes here.", TextType.TEXT)
        test_node = text_to_textnodes(node)
        self.assertListEqual(text_to_textnodes(node), [
        TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
        TextNode(" is a picture and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://example.com"),
        TextNode(" goes here.", TextType.TEXT),
        ])

    def test_text_to_textnodes5(self):
        node = TextNode("Text with _italic_, **bold**, and `code`.", TextType.TEXT)
        test_node = text_to_textnodes(node)
        self.assertListEqual(text_to_textnodes(node), [
        TextNode("Text with ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(", ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(", and ", TextType.TEXT),  
        TextNode("code", TextType.CODE),
        TextNode(".", TextType.TEXT),   
        ])

    def test_text_to_textnodes7(self):
        node = TextNode("", TextType.TEXT)
        test_node = text_to_textnodes(node)
        self.assertListEqual(text_to_textnodes(node), [])


if __name__ == "__main__":
    unittest.main()
