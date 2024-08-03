"""Package-wide utilities."""

import pdftotext


class PagesIndexError(Exception):
    """The requested page range does not exist in the pdf."""


def pdf_to_text(fpath, fp, lp, physical=False):
    """Extract text from the pdf at fpath.

    First page and last page are 1-indexed and inclusive. Physical preserves the
    physical layout of the text.
    """
    with open(fpath, "rb") as f:
        pdf = pdftotext.PDF(f, physical=physical)
        if len(pdf) < fp:
            raise PagesIndexError()
        real_lp = lp if lp <= len(pdf) else len(pdf)
        return "\n\n".join([pdf[i] for i in range(fp-1, real_lp)])
