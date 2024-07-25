"""Structural elements for all package scripts."""

import sys
import argparse
import os
from getpass import getpass


def err(message):
    """Print message to stderr and exit with code 1."""
    sys.exit(f"err: {message}")


def get_parser():
    """Make parser for universal options."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--openai-api-key", type=str, help="OpenAI API key")
    return parser


def check_opts(opts):
    """Do post-initialization checks of universal options."""
    # For api key, check option, then envvar, then ask.
    if not opts["openai_api_key"]:
        if "OPENAI_API_KEY" in os.environ:
            opts["openai_api_key"] = os.environ["OPENAI_API_KEY"]
        else:
            opts["openai_api_key"] = getpass("OpenAI API key: ")
