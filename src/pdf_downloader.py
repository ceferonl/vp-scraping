import os
import logging
from urllib.parse import urlparse
import requests
from crawl4ai.mdc import document_downloader

def setup_logger():
    logger = logging.getLogger('pdf_downloader')
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def download_pdf(url, output_dir):
    """Download a PDF file from the given URL to the output directory using Crawl4AI."""
    logger = setup_logger()
    logger.info(f"Downloading PDF from {url}")
    try:
        os.makedirs(output_dir, exist_ok=True)
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename or not filename.lower().endswith('.pdf'):
            filename = f"{hash(url)}.pdf"
        output_path = os.path.join(output_dir, filename)
        # Try Crawl4AI's document downloader
        result = document_downloader.download_document(
            url=url,
            output_path=output_path,
            document_type='pdf'
        )
        if not result.get('success'):
            logger.warning(f"Crawl4AI download failed, falling back to requests: {result.get('error')}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            result = {
                'success': True,
                'local_path': output_path,
                'filename': filename,
                'crawl4ai_fallback': True
            }
        logger.info(f"Successfully downloaded PDF to {output_path}")
        return {
            "original_url": url,
            "local_path": result.get('local_path', output_path),
            "filename": filename,
            "metadata": result.get('metadata', {}),
            "crawl4ai_fallback": result.get('crawl4ai_fallback', False)
        }
    except Exception as e:
        logger.error(f"Error downloading PDF from {url}: {str(e)}")
        return {"original_url": url, "error": str(e)}

def download_pdfs(pdf_links, output_dir):
    """Download multiple PDF files from a list of URLs."""
    results = []
    for url in pdf_links:
        result = download_pdf(url, output_dir)
        results.append(result)
    return results

if __name__ == "__main__":
    test_links = [
        "https://www.versnellingsplan.nl/files/document1.pdf",
        "https://www.versnellingsplan.nl/files/document2.pdf"
    ]
    out_dir = "output/test"
    results = download_pdfs(test_links, out_dir)
    for r in results:
        print(r)
