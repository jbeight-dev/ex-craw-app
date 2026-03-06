import json
import os
import logging
from typing import Dict, List, Union

logger = logging.getLogger(__name__)

class JsonWriter:
    def save(self, data: Union[Dict, List], file_path: str) -> bool:
        try:
            # 디렉토리가 없으면 생성
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"결과가 {file_path}에 JSON 형식으로 저장되었습니다.")
            return True
        except Exception as e:
            logger.error(f"JSON 저장 중 오류 발생: {e}")
            return False
