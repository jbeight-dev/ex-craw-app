import logging
import requests
from typing import Optional, Dict
from crawler.retry import execute_with_retry

logger = logging.getLogger(__name__)

class StaticCrawler:
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch(self, url: str, timeout: float = 10.0, retry_count: int = 3, delay: float = 1.0) -> Optional[str]:
        logger.info(f"선택된 크롤러: StaticCrawler (requests) -> {url}")
        
        def _make_request():
            return requests.get(url, headers=self.headers, timeout=timeout)
            
        try:
            response = execute_with_retry(_make_request, max_retries=retry_count, delay=delay)
            if response.status_code == 200:
                return response.text
            else:
                logger.warning(f"URL: {url} fetched with non-200 status code: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
