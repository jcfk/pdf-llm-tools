"""Entry point for all pdfllm actions"""

from . import opts
from .titler.main import main as titler_main


def main():
    """Entry point for all pdfllm actions"""
    opts.parse_options()

    if opts.opts["action"] == "titler":
        titler_main()
