import os, unittest
import pdf_llm_tools, pdf_llm_tools.utils, pdf_llm_tools.titler

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    def test_pdf_to_text(self):
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
    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    def test_get_new_fpath(self):
        fpath = "pdfs/fruits.pdf"
        meta = {"year": 1973, "authors": ["Jekyll"], "title": "Real Good!!"}
        new_fpath = pdf_llm_tools.titler.get_new_fpath(fpath, meta)
        self.assertEqual(new_fpath, "pdfs/1973-Jekyll-real-good.pdf")

    def tearDown(self):
        os.chdir(self.cwd)

class TestTitlerParse(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))

        pdf_llm_tools.titler.opts = {}
        pdf_llm_tools.titler.opts["first_page"] = 1
        pdf_llm_tools.titler.opts["last_page"] = 5
        pdf_llm_tools.titler.opts["openai_api_key"] = os.environ["OPENAI_API_KEY"]

    def test_parse_content_1(self):
        fpath = "pdfs/mdeup.pdf"
        meta = pdf_llm_tools.titler.get_pdf_metadata(fpath)
        self.assertEqual(meta["year"], 2024)
        self.assertEqual(meta["authors"], ["Krishna"])
        self.assertEqual(meta["title"], "MODULAR DEUTSCH ENTROPIC UNCERTAINTY PRINCIPLE")

    def test_parse_content_2(self):
        fpath = "pdfs/fowler.pdf"
        meta = pdf_llm_tools.titler.get_pdf_metadata(fpath)
        self.assertEqual(meta["year"], 2005)
        self.assertEqual(meta["authors"], ["Fowler"])
        self.assertEqual(meta["title"], "The Mathematics Autodidact’s Aid")

    def tearDown(self):
        os.chdir(self.cwd)

        pdf_llm_tools.titler.opts = None

# class TestTitlerFull(unittest.TestCase):