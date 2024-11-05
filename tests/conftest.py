"""Top-level pytest conftest.py"""

import os
import pytest

from . import utils


def pytest_addoption(parser):
    """Add the --openai-api-key option to the pytest argparse."""
    parser.addoption("--openai-api-key")


@pytest.fixture
def fix_openai_api_key(request):
    """Return the OpenAI API key as passed to pytest as an option."""
    api_key = request.config.getoption("--openai-api-key")
    if not api_key:
        if "OPENAI_API_KEY" in os.environ:
            api_key = os.environ["OPENAI_API_KEY"]
        else:
            utils.err("No OpenAI API key given.")
    return api_key
