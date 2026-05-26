"""Helper utilities for building Jupyter notebooks programmatically."""
import nbformat as nbf


def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip("\n"))


def code(src: str):
    return nbf.v4.new_code_cell(src.strip("\n"))


def save_notebook(cells, path):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.11",
        },
    }
    with open(path, "w") as f:
        nbf.write(nb, f)
    print(f"Wrote {path}")
