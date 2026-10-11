import sys

from generate_webpage import *
from recursive_copy import clean_folder, recursive_copy


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    clean_folder("docs")
    recursive_copy("static", "docs")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


if __name__ == "__main__":
    main()