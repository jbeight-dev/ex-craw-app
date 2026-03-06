import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class RawHtmlWriter:
    def save(self, html_content: str, file_path: str) -> bool:
        try:
            # 디렉토리가 없으면 생성
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"원본 HTML이 {file_path}에 저장되었습니다.")
            return True
        except Exception as e:
            logger.error(f"HTML 원본 저장 중 오류 발생: {e}")
            return False
