import pdftotext

def pdf_to_text(fpath, fp, lp, physical=False):
    with open(fpath, "rb") as f:
        pdf = pdftotext.PDF(f, physical=physical)
        return "\n\n".join([pdf[i] for i in range(fp-1, lp)])
