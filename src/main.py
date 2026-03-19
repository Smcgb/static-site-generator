from textnode import TextNode, TextType
def main():
	print("hello world")
	node = TextNode('This is some anchor text',TextType.ANCHOR_TEXT,' https://www.boot.dev')
	print(node)


if __name__ == "__main__":
    main()
