# Static Site Generator

A static site generator written in Python, built from scratch (as a boot.dev
project) to understand how Markdown-to-HTML pipelines work under the hood
rather than relying on an existing library.

It converts Markdown source files into a tree of HTML nodes and renders that
tree to HTML strings. It copies static assets (CSS, images) into the output
directory, renders `content/index.md` into an HTML page using `template.html`,
and serves the result locally.

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
- **Asset copying** (`src/recurisve_copy.py`) — `clean_folder` wipes the
  `public/` output directory and `recursive_copy` copies everything from
  `static/` into `public/`, recreating the directory structure (implemented
  by hand rather than with `shutil.copytree`, per the course requirements).
- **Page generation** (`src/generate_webpage.py`) — `extract_title` pulls the
  `# H1` heading out of a Markdown document, and `generate_page` converts the
  Markdown to HTML and substitutes it into `template.html` (replacing
  `{{ Title }}` and `{{ Content }}`), writing the result to `public/`.

## Project layout

```
static-site-generator/
├── main.sh           # entry point: builds the site and serves it
├── test.sh           # runs the unit test suite
├── template.html     # HTML template with {{ Title }} / {{ Content }}
├── content/          # Markdown source pages (index.md)
├── src/
│   ├── main.py              # builds the site into public/
│   ├── recurisve_copy.py    # clean_folder / recursive_copy
│   ├── generate_webpage.py  # extract_title / generate_page
│   ├── textnode.py          # TextNode/TextType + HTML conversion
│   ├── htmlnode.py          # HTMLNode/LeafNode/ParentNode
│   ├── markdown_convert.py  # Markdown parsing -> HTML node tree
│   └── test_*.py            # unittest suites for each module
├── static/           # source assets (css, images) copied verbatim
└── public/           # generated output (overwritten on each run)
```

## Usage

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/) (see
`.python-version` / `pyproject.toml`).

```sh
./main.sh
```

This deletes the existing `public/` directory, recopies everything from
`static/` into it, generates `public/index.html` from `content/index.md`, and
then serves `public/` at <http://localhost:8888>.

## Testing

```sh
./test.sh
```

Runs the full `unittest` suite under `src/` (`test_htmlnode.py`,
`test_textnode.py`, `test_markdown_converter.py`, `test_generate_webpage.py`).

## Status / TODO

- `main.py` currently renders only `content/index.md` — it doesn't yet walk
  the whole `content/` directory and render every Markdown file to a page.
- `HTMLNode` has a noted TODO to drop the shared `children`/`value`
  attributes from the base class and let `LeafNode`/`ParentNode` each define
  their own.

## AI Disclosure

All of the code in this project was written by me. Generative AI (Claude)
was used only to write this README and occasionally to answer clarifying
questions. The only AI-written changes are README edits: the initial
"Add README" commit and later README commits marked with a
`Co-Authored-By: Claude` trailer. Every code commit is entirely my own work.