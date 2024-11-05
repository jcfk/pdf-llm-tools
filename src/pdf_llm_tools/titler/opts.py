"""The titler action-options structure and parser"""

import sys
from .. import utils


opts = {
    "first_page": 1,
    "last_page": 5
}


def parse_options(i):
    """Parse sys.argv into the action_opts structure.

    i is the index in sys.argv at which parsing begins. The index is updated and
    returned."""
    argc = len(sys.argv)
    while (i < argc and sys.argv[i][0] == "-"):
        opt = sys.argv[i]
        if opt == "--first-page":
            if i+1 == argc:
                utils.err("option --first-page takes an argument")
            opts["first_page"] = sys.argv[i+1]
            i += 1
        elif opt == "--last-page":
            if i+1 == argc:
                utils.err("option --last-page takes an argument")
            opts["last_page"] = sys.argv[i+1]
            i += 1
        else:
            utils.err(f"unknown titler option {opt}")
        i += 1

    if opts["first_page"] > opts["last_page"]:
        utils.err("--first-page cannot be greater than --last-page")

    return i
