# Static Site Generator

A static site generator written in Python, built from scratch (as a boot.dev
project) to understand how Markdown-to-HTML pipelines work under the hood
rather than relying on an existing library.

It converts Markdown source files into a tree of HTML nodes and renders that
tree to HTML strings. It also handles copying static assets (CSS, images)
into the output directory.

## How it works

The pipeline is split into a few layers:

- **`TextNode` / `TextType`** (`src/textnode.py`) — represents a run of
  inline text along with its type (plain text, bold, italic, code, link,
  image). `text_node_to_html_node` converts a `TextNode` into a renderable
  HTML leaf.
- **`HTMLNode` / `LeafNode` / `ParentNode`** (`src/htmlnode.py`) — a small
  HTML AST. `LeafNode` renders a single tag with no children (e.g. `<b>`,
  `<a>`, `<img>`), and `ParentNode` renders a tag that wraps other nodes
  (e.g. `<p>`, `<ul>`, `<div>`).
- **Markdown conversion** (`src/markdown_convert.py`) — parses raw Markdown:
  - Splits inline text on delimiters (`**bold**`, `*italic*`/`_italic_`,
    `` `code` ``) and extracts Markdown links/images into `TextNode`s.
  - Splits a document into blocks (split on blank lines) and classifies each
    block (`paragraph`, `heading`, `code`, `quote`, unordered/ordered list).
  - Converts each block into the matching `ParentNode` tree
    (`markdown_to_html_node`), which can then be rendered with `.to_html()`.
- **Asset copying** (`src/main.py`) — `clean_folder` wipes the `public/`
  output directory and `recursive_copy` copies everything from `static/`
  into `public/`, recreating the directory structure (implemented by hand
  rather than with `shutil.copytree`, per the course requirements).

## Project layout

```
static-site-generator/
├── main.sh           # entry point: runs src/main.py
├── test.sh           # runs the unit test suite
├── src/
│   ├── main.py              # cleans/copies static -> public
│   ├── textnode.py          # TextNode/TextType + HTML conversion
│   ├── htmlnode.py          # HTMLNode/LeafNode/ParentNode
│   ├── markdown_convert.py  # Markdown parsing -> HTML node tree
│   └── test_*.py            # unittest suites for each module
├── static/           # source assets (css, images) copied verbatim
└── public/           # generated output (overwritten on each run)
```

## Usage

Requires Python 3.13+ (see `.python-version` / `pyproject.toml`).

```sh
./main.sh
```

This deletes the existing `public/` directory and recopies everything from
`static/` into it.

## Testing

```sh
./test.sh
```

Runs the full `unittest` suite under `src/` (`test_htmlnode.py`,
`test_textnode.py`, `test_markdown_converter.py`).

## Status / TODO

- `main.py` currently only copies static assets — it doesn't yet walk a
  `content/` directory of Markdown files and render them to HTML pages.
- `HTMLNode` has a noted TODO to drop the shared `children`/`value`
  attributes from the base class and let `LeafNode`/`ParentNode` each define
  their own.
