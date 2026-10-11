from generate_webpage import *
from recursive_copy import clean_folder, recursive_copy


def main():
    clean_folder("public")
    recursive_copy("static", "public")
    generate_pages_recursive("content/", "template.html", "public/")

if __name__ == "__main__":
    main()