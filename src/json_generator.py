import json
import os
import logging
from datetime import datetime

try:
    from crawl4ai.mdc import json_export
    CRAWL4AI_AVAILABLE = True
except ImportError:
    CRAWL4AI_AVAILABLE = False

def setup_logger():
    logger = logging.getLogger('json_generator')
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def generate_json(scraped_content, downloaded_pdfs, output_dir):
    """Generate a JSON file with metadata, content, and file links.
    Uses Crawl4AI's json_export if available, otherwise falls back to standard json.
    """
    logger = setup_logger()
    try:
        os.makedirs(output_dir, exist_ok=True)
        url = scraped_content["url"]
        filename = f"{hash(url)}.json"
        output_path = os.path.join(output_dir, filename)
        pdf_map = {pdf["original_url"]: pdf["local_path"] for pdf in downloaded_pdfs if "error" not in pdf}
        output_data = {
            "url": url,
            "metadata": scraped_content["metadata"],
            "content": scraped_content["content"],
            "files": [
                {"url": pdf_url, "local_path": pdf_map.get(pdf_url, "")} for pdf_url in scraped_content["pdf_links"]
            ],
            "scraped_at": datetime.now().isoformat()
        }
        if CRAWL4AI_AVAILABLE:
            try:
                output_path = json_export.save_document(
                    output_data,
                    output_dir=output_dir,
                    filename=filename,
                    ensure_ascii=False,
                    indent=2
                )
            except Exception as e:
                logger.warning(f"Crawl4AI json_export failed, falling back to standard json: {str(e)}")
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, ensure_ascii=False, indent=2)
                output_path = output_path + '.crawl4ai_fallback'
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Generated JSON output at {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error generating JSON output: {str(e)}")
        return None

if __name__ == "__main__":
    scraped_content = {
        "url": "https://www.versnellingsplan.nl/kennisbank/test-article",
        "metadata": {"date": "2023-01-15", "type": "Research Report"},
        "content": "This is the article content.",
        "pdf_links": ["https://example.com/test.pdf"]
    }
    downloaded_pdfs = [
        {"original_url": "https://example.com/test.pdf", "local_path": "/path/to/pdfs/test.pdf", "filename": "test.pdf"}
    ]
    out_dir = "output/test"
    output_path = generate_json(scraped_content, downloaded_pdfs, out_dir)
    print(f"Output JSON: {output_path}")
