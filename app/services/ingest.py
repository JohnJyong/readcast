import requests
import html2text
from bs4 import BeautifulSoup

def fetch_and_parse(url: str) -> dict:
    """
    Fetches URL content and returns title and clean markdown.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Simple Title Extraction
        title = soup.title.string if soup.title else url
        
        # Content Cleaning (HTML -> Markdown)
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        clean_text = h.handle(response.text)
        
        return {
            "title": title.strip(),
            "content": clean_text,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "title": "Error fetching",
            "content": str(e),
            "status": "error"
        }
