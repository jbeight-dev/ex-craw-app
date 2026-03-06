import time
import logging
import requests
from typing import Callable

logger = logging.getLogger(__name__)

def execute_with_retry(make_request: Callable[[], requests.Response], max_retries: int = 3, delay: float = 1.0) -> requests.Response:
    last_exception = None
    for attempt in range(1, max_retries + 1):
        try:
            response = make_request()
            
            # HTTP 4xx (클라이언트 에러) -> 재시도 없이 반환
            if 400 <= response.status_code < 500:
                logger.error(f"HTTP {response.status_code} Client Error for URL: {response.url}. No retry.")
                return response
            
            # HTTP 5xx (서버 에러) -> 재시도
            if 500 <= response.status_code < 600:
                logger.warning(f"HTTP {response.status_code} Server Error. Attempt {attempt}/{max_retries}")
                if attempt < max_retries:
                    time.sleep(delay)
                continue
                
            return response
            
        except requests.exceptions.Timeout as e:
            logger.warning(f"Timeout Error. Attempt {attempt}/{max_retries}")
            last_exception = e
            if attempt < max_retries:
                time.sleep(delay)
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Network Error: {e}. Attempt {attempt}/{max_retries}")
            last_exception = e
            if attempt < max_retries:
                time.sleep(delay)
                
    if last_exception:
        logger.error("Max retries reached due to network/timeout error.")
        raise last_exception
    else:
        # 5xx 응답이 지속된 경우
        logger.error("Max retries reached due to persistent 5xx errors.")
        return response
