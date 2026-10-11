from generate_webpage import *
from recurisve_copy import clean_folder, recursive_copy


def main():

	clean_folder("public")
	recursive_copy("static", "public")
	generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
