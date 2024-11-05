"""Package-wide utilities"""

import sys
import pdftotext


class PagesIndexError(Exception):
    """The requested page range does not exist in the PDF."""


def err(message):
    """Print message to stderr and exit with code 1."""
    sys.exit(f"err: {message}")


def show_help_and_exit():
    """Print usage and exit with code 0.""" 
    print("todo")
    sys.exit(0)


def extract_text(fpath, first_page, last_page, physical=False):
    """Extract text from the PDF at fpath and return as string.

    first_page and last_page are 1-indexed and inclusive. physical preserves the
    physical layout of the text.
    """
    with open(fpath, "rb") as f:
        pdf = pdftotext.PDF(f, physical=physical)
        if len(pdf) < first_page:
            raise PagesIndexError()
        real_last_page = last_page if last_page <= len(pdf) else len(pdf)
        return "\n\n".join([pdf[i] for i in range(first_page-1, real_last_page)])
