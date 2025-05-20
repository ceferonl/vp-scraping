# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`vp-scraping` is a web scraping project for extracting content from the Versnellingsplan Kennisbank website. It uses Crawl4AI for advanced scraping, content extraction, and PDF downloading, with Polars for data processing.

## Commands

### Setup and Installation

```bash
# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Running the Scraper

```bash
# Run the main scraper (production mode)
python src/main.py

# Run the scraper in demo mode (with sample URLs)
cd scripts
python -m quarto render scraper-demo.qmd
```

### Testing and Linting

```bash
# Run linting checks
ruff check .

# Run tests
pytest tests/
```

## Architecture

The project follows a modular pipeline architecture:

1. **URL Extraction** (`url_extractor.py`): Extracts content URLs from the knowledge base main page
2. **Content Scraping** (`content_scraper.py`): Scrapes content from individual pages using Crawl4AI
3. **PDF Downloading** (`pdf_downloader.py`): Downloads linked PDF files from content pages
4. **JSON Generation** (`json_generator.py`): Generates structured JSON output with content and file references

Each module can be used independently for testing or in combination as part of the full pipeline. The main entry point (`src/main.py`) orchestrates the complete workflow.

## Output Structure

The project saves results to the `output/` directory with the following organization:
- `output/demo/`: Results from demo runs
- `output/test/`: Results from test runs
- `output/production/`: Results from production runs

## Dependencies

Key dependencies include:
- Crawl4AI: Advanced web crawling framework with MDC (metadata and content) selectors
- Polars: Fast data processing
- Requests: Used as fallback for web requests

## Development Notes

- The project uses Python 3.12+ and follows standard Python packaging conventions
- The code is linted with Ruff with a line length of 88 characters
- All modules include a `setup_logger()` function for consistent logging
- Each module can be run independently for testing (with `if __name__ == "__main__"` blocks)
- The `scripts/` directory contains demonstration notebooks in Quarto format
- Crawl4AI's MDC selectors are used for standardized content extraction