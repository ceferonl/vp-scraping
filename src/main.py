import logging
import os
from url_extractor import extract_content_urls
from content_scraper import scrape_content
from pdf_downloader import download_pdfs
from json_generator import generate_json

def setup_logger():
    logger = logging.getLogger('main_scraper')
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def main():
    logger = setup_logger()
    base_url = "https://www.versnellingsplan.nl/kennisbank/"
    output_dir = "output/production"
    logger.info("Extracting content URLs...")
    urls = extract_content_urls(base_url)
    logger.info(f"Found {len(urls)} content URLs.")
    for idx, url in enumerate(urls, 1):
        logger.info(f"[{idx}/{len(urls)}] Scraping content: {url}")
        scraped = scrape_content(url)
        if 'error' in scraped:
            logger.error(f"Failed to scrape {url}: {scraped['error']}")
            continue
        pdf_links = scraped.get('pdf_links', [])
        if pdf_links:
            logger.info(f"Downloading {len(pdf_links)} PDFs for {url}")
            pdfs = download_pdfs(pdf_links, os.path.join(output_dir, "pdfs"))
        else:
            pdfs = []
        json_path = generate_json(scraped, pdfs, output_dir)
        logger.info(f"Saved JSON: {json_path}")
    logger.info("Scraping complete.")

if __name__ == "__main__":
    main()
