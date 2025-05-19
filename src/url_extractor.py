import logging
from crawl4ai import Crawler


def setup_logger():
    logger = logging.getLogger('url_extractor')
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def extract_content_urls(base_url="https://www.versnellingsplan.nl/kennisbank/"):
    """Extract all content URLs from the main knowledge base page using Crawl4AI."""
    logger = setup_logger()
    logger.info(f"Extracting content URLs from {base_url}")
    try:
        crawler = Crawler()
        page = crawler.fetch(base_url)
        # Adjust selector as needed for the actual site structure
        content_links = page.select('a.content-link')
        urls = [link.get('href') for link in content_links if link.get('href')]
        # Ensure URLs are absolute
        urls = [url if url.startswith('http') else f"{base_url.rstrip('/')}/{url.lstrip('/')}" for url in urls]
        logger.info(f"Found {len(urls)} content URLs")
        return urls
    except Exception as e:
        logger.error(f"Error extracting content URLs: {str(e)}")
        return []


if __name__ == "__main__":
    urls = extract_content_urls()
    print(f"Extracted {len(urls)} URLs:")
    for url in urls:
        print(url)
