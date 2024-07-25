"""The 'pdfllm-titler' pdf renaming utility."""

import argparse
import json
import re
import os
from . import base, utils, llm

opts = None


def get_parser():
    """Make parser for titler script options."""
    parser = argparse.ArgumentParser(
        description="Rename PDF documents according to their contents.",
        parents=[base.get_parser()])
    parser.add_argument("--first-page", "-f", type=int, default=1,
                        help="First page of pdf to read (default: 1)")
    parser.add_argument("--last-page", "-l", type=int, default=5,
                        help="Last page of pdf to read (default: 5)")
    parser.add_argument("fpath", type=str, nargs="+", help="PDF to rename")
    return parser


def make_opts():
    """Parse script args and initialize opts dictionary."""
    global opts

    parser = get_parser()
    opts = vars(parser.parse_args())
    base.initialize_opts(opts)


def llm_parse_metadata(text, pdf_name):
    """Parse metadata from the given pdf text with a helpful assistant LLM.
    Return the response as a json object."""
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


def get_new_fpath(fpath, meta):
    """Create new fpath from extracted pdf metadata."""
    fdir = fpath[:fpath.rfind("/")+1]
    year = meta["year"]
    author = meta["authors"][0]
    author = author[0].upper() + author[1:].lower()
    title = meta["title"].lower().replace(" ", "-")
    new_fname = re.sub(r"[^a-zA-Z0-9-.]", r"", f"{year}-{author}-{title}.pdf")
    return f"{fdir}{new_fname}"


def main():
    """Execute titler."""
    make_opts()

    for fpath in opts["fpath"]:
        # Extract data from pdf
        try:
            text = utils.pdf_to_text(fpath, opts["first_page"], opts["last_page"])
        except utils.PagesIndexError:
            print(f"Given --first-page {opts['first_page']} and --last-page"
                  f" {opts['last_page']} are outside of {fpath}; skipping")
            continue
        pdf_name = fpath[fpath.rfind("/")+1:]

        # Parse out metadata
        meta = llm_parse_metadata(text, pdf_name)
        if not meta:
            print(f"Unable to read metadata from {fpath}; skipping")
            continue

        # Create new filename
        new_fpath = get_new_fpath(fpath, meta)

        # Rename
        os.rename(fpath, new_fpath)
        print(f"Renamed {fpath} to {new_fpath}")
