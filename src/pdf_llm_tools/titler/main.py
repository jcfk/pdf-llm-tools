"""The 'titler' PDF renaming utility"""

import os
import re
from .. import llm
from .. import utils
from ..opts import opts


def is_valid_metadata(parsed_data):
    """Check that llm output is useable metadata.

    A simple check that it conforms to the titler metadata "schema", and that
    the error field is not set. Because I don't want to use JSON Schema."""
    for key in ["year", "authors", "title", "error"]:
        if key not in parsed_data.keys():
            return False

    return not parsed_data["error"]


def parse_metadata(raw_data):
    """Parse metadata from the given PDF text via LLM.

    raw_data is a dictionary of the form

    { "filename": "mypdf.pdf", "text": "pdf text here" }

    Return a metadata dictionary of the form

    {
     "year": 2001,
     "authors": ["Obama", "Trump", "Biden"],
     "title": "How to Train Your Dragon",
     "error": False
    }
    """
    filename = raw_data["filename"]
    text = raw_data["text"]
    message = ("Detect the metadata for year, author surnames, and title from"
               " the following text of the first pages of an academic paper or"
               " book. I will also provide the filename."
               " Format your response as a json object, where 'year' is an int,"
               " 'authors' is a list of surname strings, 'title' is a string,"
               " and 'error' is a boolean that is true if you fail to complete"
               " the task and false otherwise."
               f" Here is the filename: '{filename}'."
               f" Here is the text: {text}.")

    parsed_data = llm.helpful_assistant_json(message)
    return parsed_data if is_valid_metadata(parsed_data) else None


def get_new_fpath(fpath, parsed_data):
    """Create new fpath from extracted PDF metadata."""
    fdir = fpath[:fpath.rfind("/")+1]
    year = parsed_data["year"]
    author = parsed_data["authors"][0]
    author = author[0].upper() + author[1:].lower()
    title = parsed_data["title"].lower().replace(" ", "-")
    new_fname = re.sub(r"[^a-zA-Z0-9-.]", r"", f"{year}-{author}-{title}.pdf")
    return f"{fdir}{new_fname}"


def title_file(fpath):
    """Extract and parse text from fpath, and rename."""
    # Handle PDF not existing/readable exceptions?
    # Extract text/name from PDF
    raw_data = {"filename": fpath[fpath.rfind("/")+1:]}
    try:
        # no physical=True?
        raw_data["text"] = utils.extract_text(fpath, opts["actopts"]["first_page"],
                                              opts["actopts"]["last_page"])
    except utils.PagesIndexError:
        print(f"Chosen --first-page {opts["actopts"]["first_page"]} and --last-page"
              f" {opts["actopts"]["last_page"]} are outside of {fpath}; skipping")
        return

    # Parse out metadata
    parsed_data = parse_metadata(raw_data)
    if not parsed_data:
        print(f"Unable to read metadata from {fpath}; skipping")
        return

    # Create new filename
    new_fpath = get_new_fpath(fpath, parsed_data)

    # Rename
    os.rename(fpath, new_fpath)
    print(f"Renamed {fpath} to {new_fpath}")


def main():
    """Extract metadata from the given files and rename them accordingly."""
    for fpath in opts["files"]:
        title_file(fpath)
