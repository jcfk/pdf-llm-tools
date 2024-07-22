import argparse, os
from getpass import getpass

# def err(message):
#     sys.exit(message)

def get_base_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--openai-api-key", type=str, help="OpenAI API key")
    return parser

def initialize_base_opts(opts):
    # For api key, check option, then envvar, then ask.
    if not opts.openai_api_key:
        if "OPENAI_API_KEY" in os.environ:
            opts.openai_api_key = os.environ["OPENAI_API_KEY"]
        else:
            opts.openai_api_key = getpass("OpenAI API key: ")
