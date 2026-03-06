import csv
import os
import logging
from typing import Dict, List, Union

logger = logging.getLogger(__name__)

class CsvWriter:
    def save(self, data: Union[Dict, List], file_path: str) -> bool:
        if not data:
            logger.warning("저장할 데이터가 없습니다.")
            return False

        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            # 단일 Dict인 경우 리스트로 변환
            if isinstance(data, dict):
                data = [data]

            if not isinstance(data, list) or len(data) == 0:
                logger.warning("유효하지 않은 데이터 형식입니다. 리스트 또는 딕셔너리여야 합니다.")
                return False

            # 모든 가능한 키를 수집하여 헤더로 사용
            headers = []
            for item in data:
                if isinstance(item, dict):
                    for key in item.keys():
                        if key not in headers:
                            headers.append(key)
            
            if not headers:
                logger.warning("데이터에서 헤더를 추출할 수 없습니다.")
                return False

            # DictWriter를 사용해 CSV 작성
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                
                for row in data:
                    # 다건 추출 결과(리스트)가 밸류로 들어올 수 있으므로 문자열 처리
                    processed_row = {}
                    for k, v in row.items():
                        if isinstance(v, list):
                            processed_row[k] = " | ".join(str(item) for item in v)
                        else:
                            processed_row[k] = v
                    writer.writerow(processed_row)
            
            logger.info(f"결과가 {file_path}에 CSV 형식으로 저장되었습니다.")
            return True
            
        except Exception as e:
            logger.error(f"CSV 저장 중 오류 발생: {e}")
            return False
