from textnode import TextNode
from textnode import TextType

def main():
    a = TextNode("This is some another text", TextType.LINK, "http://google.com")
    print(a)
 
main()
