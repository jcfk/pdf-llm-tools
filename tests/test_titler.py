"""All tests for pdf-llm-tools."""

import os.path
import shutil
import subprocess
import tempfile

import pytest

from . import utils


TITLER_TEST_PDF_PARAMS = [
    ("fowler.pdf", "2005-Fowler-the-mathematics-autodidacts-aid.pdf"),
    ("mdeup.pdf", "2024-Krishna-modular-deutsch-entropic-uncertainty-principle.pdf")
]
TMPDIR_PREFIX = "pdfllmtools_test_"


@pytest.fixture(params=TITLER_TEST_PDF_PARAMS)
def fix_tmp_pdf_params(request):
    """Copy a PDF into a temp dir for testing and yield the path.

    Clean up the temp dir and the PDF after yield."""
    # Could use pytest built-in tmp_path_factory?

    pdf_name, expected_fname = request.param

    pdf_fpath = utils.get_resource_abs_path(pdf_name)
    tmpdir = tempfile.TemporaryDirectory(prefix=TMPDIR_PREFIX)
    tmp_pdf_fpath = shutil.copy(pdf_fpath, tmpdir.name)

    yield tmp_pdf_fpath, expected_fname

    # is explicit cleanup necessary?
    tmpdir.cleanup()


def test_titler_full(fix_tmp_pdf_params, fix_openai_api_key):
    """Test that the command `pdfllm titler` titles PDFs correctly.

    This is a front to back test that should have 100% coverage for titler."""
    tmp_pdf_fpath, expected_fname = fix_tmp_pdf_params
    tmpdir = os.path.dirname(tmp_pdf_fpath)

    cp = subprocess.run(["pdfllm",
                         "--openai-api-key", fix_openai_api_key,
                         "titler",
                         tmp_pdf_fpath])

    assert cp.returncode == 0, "`pdfllm titler` did not run succesfully"
    assert expected_fname in os.listdir(tmpdir)
