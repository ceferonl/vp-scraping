import logging
import crawl4ai
import asyncio


def setup_logger():
    logger = logging.getLogger('url_extractor')
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


async def extract_content_urls_async(base_url="https://www.versnellingsplan.nl/kennisbank/"):
    """Extract all content URLs from the main knowledge base page using Crawl4AI's AsyncWebCrawler."""
    logger = setup_logger()
    logger.info(f"Extracting content URLs from {base_url} (Crawl4AI)")
    try:
        async with crawl4ai.AsyncWebCrawler() as crawler:
            page = await crawler.arun(url=base_url)
            # Wait for the content links to appear (10s timeout)
            await page.wait_for('a.elementor-post__thumbnail__link', timeout=10000)
            # Print the first 2000 chars of the rendered HTML for debugging
            print(page.html[:2000])
            # Extract the links
            links = page.soup.select('a.elementor-post__thumbnail__link')
            urls = [link.get('href') for link in links if link.get('href')]
            urls = [url if url.startswith('http') else f"{base_url.rstrip('/')}/{url.lstrip('/')}" for url in urls]
            logger.info(f"Found {len(urls)} content URLs")
            return urls
    except Exception as e:
        logger.error(f"Error extracting content URLs: {str(e)}")
        return []


def extract_content_urls(base_url="https://www.versnellingsplan.nl/kennisbank/"):
    """Sync wrapper for extract_content_urls_async for compatibility."""
    try:
        return asyncio.run(extract_content_urls_async(base_url))
    except RuntimeError:
        # If already in an event loop (e.g., Jupyter), use nest_asyncio
        import nest_asyncio
        nest_asyncio.apply()
        return asyncio.get_event_loop().run_until_complete(extract_content_urls_async(base_url))


if __name__ == "__main__":
    urls = extract_content_urls()
    print(f"Extracted {len(urls)} URLs:")
    for url in urls:
        print(url)
