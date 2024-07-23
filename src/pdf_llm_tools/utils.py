import pdftotext

class PagesIndexError(Exception):
    pass

def pdf_to_text(fpath, fp, lp, physical=False):
    with open(fpath, "rb") as f:
        pdf = pdftotext.PDF(f, physical=physical)
        if len(pdf) < fp:
            raise PagesIndexError()
        real_lp = lp if lp <= len(pdf) else len(pdf)
        return "\n\n".join([pdf[i] for i in range(fp-1, real_lp)])
