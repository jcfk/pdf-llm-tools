# pdf-llm-tools

`pdf-llm-tools` is a family of AI pdf utilities:

- `pdfllm-titler` renames a pdf with metadata parsed from the filename and
  contents. In particular it renames it as `YEAR-AUTHOR-TITLE.pdf`.
- (todo) `pdfllm-toccer` adds a bookmark structure parsed from the detected
  contents table of the pdf.

We currently use poppler/[pdftotext](https://github.com/jalan/pdftotext) for
layout-preserving text extraction and PyMuPDF to update outlines. OpenAI's
`gpt-3.5-turbo-1106` is hardcoded as the LLM backend. The program requires an
OpenAI API key via option, envvar, or manual input.

## Installation

```
pip install pdf-llm-tools
```

## Usage

These utilities require all PDFs to have a correct OCR layer. Run something like
[OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) if needed.

### pdfllm-titler

```
pdfllm-titler a.pdf b.pdf c.pdf
pdfllm-titler --last-page 8 d.pdf
```

See `--help` for full details.

## Development

This project is made with [Hatch](https://hatch.pypa.io/dev/).

- Build: `hatch build`
- Test: `hatch run test:test`
