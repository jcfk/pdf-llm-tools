import sys, subprocess, argparse, os
import pdftotext
from getpass import getpass

def err(message):
    sys.exit(message)

def get_parent_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--openai-api-key", type=str, help="OpenAI API key")

    return parser

def get_opts(parser):
    opts = parser.parse_args()

    if not opts.openai_api_key:
        if "OPENAI_API_KEY" in os.environ:
            opts.openai_api_key = os.environ["OPENAI_API_KEY"]
        else:
            opts.openai_api_key = getpass("OpenAI API key: ")

    return opts

def pdf_fpath_to_text(fpath, fp, lp):
    with open(fpath, "rb") as f:
        pdf = pdftotext.PDF(f)
        return "\n\n".join([pdf[i] for i in range(fp-1, lp)])

