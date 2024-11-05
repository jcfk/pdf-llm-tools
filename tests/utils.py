"""Utilities for all tests."""

import os.path

import pytest


def err(msg):
    """Exit pytest testing with msg."""
    pytest.exit(msg, 1)


def get_resource_abs_path(name):
    """Convert resource name into absolute path.

    Resource name is a relative path under tests/resources.

    Using filesystem-based resource navigation because PDF tests rely on the
    filesystem anyways."""
    return os.path.join(os.path.dirname(__file__), "resources", name)
