# pdf-llm-tools [![PyPI](https://img.shields.io/pypi/v/pdf-llm-tools)](https://pypi.org/project/pdf-llm-tools/)

`pdf-llm-tools` is a family of AI PDF utilities:

- `pdfllm-titler` renames a PDF with metadata parsed from the filename and
  contents. In particular it renames it as `YEAR-AUTHOR-TITLE.pdf`.
- (todo) `pdfllm-toccer` adds a bookmark structure parsed from the detected
  contents table of the PDF.

We currently use poppler/[pdftotext](https://github.com/jalan/pdftotext) for
layout-preserving text extraction and PyMuPDF to update outlines. OpenAI's
`gpt-4o-mini` is hardcoded as the LLM backend. The program requires an OpenAI
API key via option, envvar, or manual input.

## Installation

```
pip install pdf-llm-tools
```

## Usage

These utilities require all PDFs to have a correct OCR layer. Run something like
[OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) if needed.

### titler

```
pdfllm titler a.pdf b.pdf c.pdf
pdfllm titler --last-page 8 d.pdf
```

See `--help` for full details.

## Development

This project is made with [Hatch](https://hatch.pypa.io/dev/).

- Build: `hatch build`
- Test: `hatch run test:test_all [--openai-api-key KEY]`
  - The test system has the same API key handling as the main progam. The key
    must be given either as an option in the `hatch run` invocation (which takes
    precedence) or as the envvar `OPENAI_API_KEY`.
