import logging
from crawl4ai import Crawler
import crawl4ai.mdc as mdc

def setup_logger():
    logger = logging.getLogger('content_scraper')
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def scrape_content(url):
    """Scrape content from a single URL, handling different layouts using Crawl4AI."""
    logger = setup_logger()
    logger.info(f"Scraping content from {url}")
    try:
        crawler = Crawler()
        page = crawler.fetch(url)
        # Extract metadata using MDC selectors if available
        metadata = {}
        date_elem = page.select_one(getattr(mdc, 'SELECTORS', {}).get('publication_date', '.publication-date'))
        if date_elem:
            metadata['date'] = date_elem.text.strip()
        type_elem = page.select_one(getattr(mdc, 'SELECTORS', {}).get('content_type', '.content-type'))
        if type_elem:
            metadata['type'] = type_elem.text.strip()
        # Extract main content
        content_selector = getattr(mdc, 'SELECTORS', {}).get('main_content', '.content-area p, .content-area h1, .content-area h2, .content-area h3, .content-area li')
        content_elements = page.select(content_selector)
        content = "\n".join([elem.text.strip() for elem in content_elements])
        # Extract hidden content (e.g., tabs/buttons)
        tab_selector = getattr(mdc, 'SELECTORS', {}).get('tab_content', '.tab-content')
        tab_contents = page.select(tab_selector)
        if tab_contents:
            content += "\n" + "\n".join([tab.text.strip() for tab in tab_contents])
        # Extract PDF links
        pdf_links = []
        for link in page.find_all('a'):
            href = link.get('href', '')
            if href.lower().endswith('.pdf'):
                if not href.startswith('http'):
                    href = f"{url.rstrip('/')}/{href.lstrip('/')}"
                pdf_links.append(href)
        result = {
            "url": url,
            "metadata": metadata,
            "content": content,
            "pdf_links": pdf_links
        }
        return result
    except Exception as e:
        logger.error(f"Error scraping content from {url}: {str(e)}")
        return {"url": url, "error": str(e)}

if __name__ == "__main__":
    test_url = "https://www.versnellingsplan.nl/kennisbank/some-article"
    result = scrape_content(test_url)
    print(result)
