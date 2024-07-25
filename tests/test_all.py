"""All tests for pdf-llm-tools."""

import os
import unittest
import pdf_llm_tools
import pdf_llm_tools.utils
import pdf_llm_tools.titler


class TestUtils(unittest.TestCase):
    """Test package-wide utilities."""
    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    def test_pdf_to_text(self):
        """Test pdf_to_text with different page ranges."""
        fpath = "pdfs/fruits.pdf"

        first_three_pages = pdf_llm_tools.utils.pdf_to_text(fpath, 1, 3)
        self.assertIn("apple", first_three_pages)
        self.assertIn("banana", first_three_pages)
        self.assertIn("carrot", first_three_pages)
        self.assertNotIn("dragonfruit", first_three_pages)

        last_three_pages = pdf_llm_tools.utils.pdf_to_text(fpath, 3, 5)
        self.assertNotIn("banana", last_three_pages)
        self.assertIn("carrot", last_three_pages)
        self.assertIn("dragonfruit", last_three_pages)
        self.assertIn("eggplant", last_three_pages)

    def tearDown(self):
        os.chdir(self.cwd)


class TestTitlerFpath(unittest.TestCase):
    """Test titler fpath utilities."""
    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    def test_get_new_fpath(self):
        """Test new fpath creation from metadata."""
        fpath = "pdfs/fruits.pdf"
        meta = {"year": 1973, "authors": ["Jekyll"], "title": "Real Good!!"}
        new_fpath = pdf_llm_tools.titler.get_new_fpath(fpath, meta)
        self.assertEqual(new_fpath, "pdfs/1973-Jekyll-real-good.pdf")

    def tearDown(self):
        os.chdir(self.cwd)


class TestTitlerParse(unittest.TestCase):
    """Test titler core metadata parsing."""
    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))

        self.opts = {}
        self.opts["first_page"] = 1
        self.opts["last_page"] = 5
        self.opts["openai_api_key"] = os.environ["OPENAI_API_KEY"]
        pdf_llm_tools.titler.opts = self.opts

    def test_parse_content_1(self):
        """Test core metadata parsing, example 1."""
        fpath = "pdfs/mdeup.pdf"
        text = pdf_llm_tools.utils.pdf_to_text(
            fpath, self.opts["first_page"], self.opts["last_page"])
        pdf_name = fpath[fpath.rfind("/")+1:]
        meta = pdf_llm_tools.titler.llm_parse_metadata(text, pdf_name)

        self.assertEqual(meta["year"], 2024)
        self.assertEqual(meta["authors"], ["Krishna"])
        self.assertEqual(meta["title"], "MODULAR DEUTSCH ENTROPIC UNCERTAINTY PRINCIPLE")

    def test_parse_content_2(self):
        """Test core metadata parsing, example 2."""
        fpath = "pdfs/fowler.pdf"
        text = pdf_llm_tools.utils.pdf_to_text(
            fpath, self.opts["first_page"], self.opts["last_page"])
        pdf_name = fpath[fpath.rfind("/")+1:]
        meta = pdf_llm_tools.titler.llm_parse_metadata(text, pdf_name)

        self.assertEqual(meta["year"], 2005)
        self.assertEqual(meta["authors"], ["Fowler"])
        self.assertEqual(meta["title"], "The Mathematics Autodidact’s Aid")

    def tearDown(self):
        os.chdir(self.cwd)

        pdf_llm_tools.titler.opts = None

# class TestTitlerFull(unittest.TestCase):
