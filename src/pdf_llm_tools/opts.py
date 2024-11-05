"""The global options structure and parser"""

import sys
import os
import getpass
from . import utils
from .titler import opts as titler_opts


opts = {
    # global command-line options
    "openai_api_key": None,

    # meta
    "action": None,
    "actopts": {},  # These need to be initialized like this or else there will
    "files": []     # be pylint E1136, E1133 elsewhere.
}
i = 1  # Initialize the global working index after the program name in sys.argv.


def parse_global_options():
    """Parse global options in sys.argv into opts.

    Parsing of sys.argv will end upon encountering a position argument or the
    end of the list.

    Update the global working index in sys.argv."""
    global i

    argc = len(sys.argv)
    while (i < argc and sys.argv[i][0] == "-"):
        opt = sys.argv[i]
        if opt == "--openai-api-key":
            if i+1 == argc:
                utils.err("option --openai-api-key takes an argument")
            opts["openai_api_key"] = sys.argv[i+1]
            i += 1
        elif opt == "--help":
            utils.show_help_and_exit()
        else:
            utils.err(f"unknown global option {opt}")
        i += 1


def parse_action_options():
    """Route to the option parser for the given action and place into opts.

    Update the global working index in sys.argv."""
    global i

    argc = len(sys.argv)
    if i == argc:
        utils.err("action required, see usage")

    if sys.argv[i] in ["titler"]:
        opts["action"] = sys.argv[i]
    else:
        utils.err(f"unknown action {sys.argv[i]}")
    i += 1

    if opts["action"] == "titler":
        i = titler_opts.parse_options(i)
        opts["actopts"] = titler_opts.opts


def check_openai_api_key():
    """If no OpenAI API key is provided, get the envvar or prompt user."""
    if not opts["openai_api_key"]:
        if "OPENAI_API_KEY" in os.environ:
            opts["openai_api_key"] = os.environ["OPENAI_API_KEY"]
        else:
            opts["openai_api_key"] = getpass.getpass("OpenAI API key: ")


def parse_options():
    """Completely parse sys.argv into the global opts structure.

    The option parsers conduct both syntactic checks (option existence, optarg
    existence) and semantic checks (option validity). Some semantic checks, like
    check_openai_api_key are kept to the end for UX purposes."""
    parse_global_options()
    parse_action_options()

    argc = len(sys.argv)
    if i == argc:
        utils.err("files required, see usage")
    opts["files"] = sys.argv[i:]

    check_openai_api_key()
