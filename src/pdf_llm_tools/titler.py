import argparse, json, re, os

from . import base, utils, llm

def make_opts():
    parser = argparse.ArgumentParser(
        description="Rename PDF documents according to their contents.",
        parents=[base.get_parser()])
    parser.add_argument("--first-page", "-f", type=int, default=1,
                        help="First page of pdf to read (default: 1)")
    parser.add_argument("--last-page", "-l", type=int, default=5,
                        help="Last page of pdf to read (default: 5)")
    parser.add_argument("fpath", type=str, nargs="+", help="PDF to rename")

    # Initialize options
    global opts
    opts = vars(parser.parse_args())
    base.initialize_opts(opts)

def llm_parse_metadata(pdf_name, text):
    message = ("Detect the metadata for year, author surnames, and title from"
               " the following text of the first pages of an academic paper or"
               " book. I will also provide the filename."
               " Format your response as a json object, where 'year' is an int,"
               " 'authors' is a list of surname strings, 'title' is a string,"
               " and 'error' is a boolean true if and only if you fail to"
               " complete the task."
               f" Here is the filename: '{pdf_name}'."
               f" Here is the text: {text}.")

    meta = json.loads(llm.helpful_assistant(message, opts["openai_api_key"]))
    return None if meta["error"] else meta

def get_pdf_metadata(fpath):
    fname = fpath[fpath.rfind("/")+1:]
    text = utils.pdf_to_text(fpath, opts["first_page"], opts["last_page"])
    return llm_parse_metadata(fname, text)

def get_new_fpath(fpath, meta):
    fdir = fpath[:fpath.rfind("/")+1]
    year = meta["year"]
    author = meta["authors"][0]
    author = author[0].upper() + author[1:].lower()
    title = meta["title"].lower().replace(" ", "-")
    new_fname = re.sub(r"[^a-zA-Z0-9-.]", r"", f"{year}-{author}-{title}.pdf")
    return f"{fdir}{new_fname}"

def main():
    make_opts()

    for fpath in opts["fpath"]:
        # Parse metadata
        try:
            meta = get_pdf_metadata(fpath)
            if not meta:
                print(f"Unable to read metadata from {fpath}; skipping")
                continue
        except utils.PagesIndexError:
            fp = opts["first_page"]
            lp = opts["last_page"]
            print(f"Given --first-page {fp} and --last-page {lp} are outside of {fpath}; skipping")
            continue

        # Create new filename
        new_fpath = get_new_fpath(fpath, meta)

        # Rename
        os.rename(fpath, new_fpath)
        print(f"Renamed {fpath} to {new_fpath}")
