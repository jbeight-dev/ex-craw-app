import logging
from typing import Optional, Dict
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

class DynamicCrawler:
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        self.headers = headers or {}
        # User-Agent는 Playwright에서 BrowserContext를 생성할 때 주입해야 함

    def fetch(self, url: str, timeout: float = 30.0, retry_count: int = 3, delay: float = 1.0) -> Optional[str]:
        """
        Playwright를 사용하여 JavaScript가 렌더링된 후의 최종 원본 HTML을 반환합니다.
        """
        logger.info(f"선택된 크롤러: DynamicCrawler (Playwright) -> {url}")
        
        # Playwright 내부에서의 TimeOut 에러 등은 자체 예외 처리가 필요합니다.
        # timeout 파라미터는 초 단위로 들어오므로 밀리초(ms)로 변환
        timeout_ms = int(timeout * 1000)
        
        # 재시도 루프 (단순화된 형태) -> Playwright 내장 retry/wait 메커니즘을 함께 사용해도 좋음
        for attempt in range(1, retry_count + 1):
            try:
                with sync_playwright() as p:
                    # headless=True: 백그라운드 환경에서 브라우저 실행 (화면 안보임)
                    browser = p.chromium.launch(headless=True)
                    
                    # 브라우저 컨텍스트 생성 시 공통 헤더 주입 가능
                    context = browser.new_context(
                        user_agent=self.headers.get("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
                        extra_http_headers={k: v for k, v in self.headers.items() if k.lower() != 'user-agent'}
                    )
                    
                    page = context.new_page()
                    
                    # 네트워크가 'networkidle' 상태가 될 때까지(추가적인 네트워크 요청이 거의 없을 때까지) 기다림
                    # 동적 페이지(React, Vue 등)의 데이터를 확실히 받아오기 위함
                    logger.debug(f"[Attempt {attempt}/{retry_count}] 페이지 로드 중(네트워크 유휴 대기)...")
                    response = page.goto(url, wait_until="networkidle", timeout=timeout_ms)
                    
                    # 지연 시간이 필요하다면 추가 대기 (페이지 내 애니메이션이나 늦게 뜨는 팝업 등 대처)
                    if delay > 0:
                        page.wait_for_timeout(int(delay * 1000))

                    if not response:
                        logger.warning(f"URL: {url} 로드 실패 (응답이 없음)")
                        browser.close()
                        continue
                        
                    if not response.ok:
                        logger.warning(f"URL: {url} 상태 코드 에러: {response.status}")
                        # 4xx 묶음 등은 필요에 따라 즉시 종료(break) 처리 가능
                    
                    # 최종 렌더링된 HTML 소스 습득
                    html_code = page.content()
                    browser.close()
                    
                    return html_code
                    
            except Exception as e:
                logger.warning(f"Playwright 크롤링 에러 발생 ({url}) - Attempt {attempt}/{retry_count}: {e}")
                if attempt == retry_count:
                    logger.error(f"최대 재시도 횟수 초과. 크롤링 실패: {url}")
                    return None
                
        return None
