import argparse
import yaml
import sys
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("crawler_config")

def load_yaml_config(config_path: str) -> Dict[str, Any]:
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"설정 파일({config_path})을 읽는 중 오류가 발생했습니다: {e}")
        sys.exit(1)

def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def parse_args_and_load_config() -> Tuple[argparse.Namespace, Dict[str, Any], list]:
    parser = argparse.ArgumentParser(description="웹 크롤링 및 데이터 추출 도구")
    parser.add_argument("--url", help="단일 URL 크롤링")
    parser.add_argument("--url-file", help="다중 URL 처리를 위한 파일 (예: urls.txt)")
    parser.add_argument("--config", help="추출 규칙 정의 YAML 파일 경로", default="config/rules.yaml")
    parser.add_argument("--output", help="출력 형식 오버라이드 (json/csv)", choices=["json", "csv"])
    parser.add_argument("--render-js", action="store_true", help="JavaScript 렌더링 사용 여부")
    parser.add_argument("--delay", type=float, help="요청 간 딜레이(초)")
    parser.add_argument("--stdout", action="store_true", help="결과를 표준 출력으로 표시")

    args = parser.parse_args()

    if not args.url and not args.url_file:
        parser.error("--url 또는 --url-file 옵션을 통해 크롤링할 대상을 지정해야 합니다.")

    # 1. 설정 로드
    config = {}
    if args.config:
        config = load_yaml_config(args.config)
        logger.info(f"설정 파일 로드 완료: {args.config}")

    urls = []
    if args.url:
        urls.append(args.url)
    elif args.url_file:
        try:
            with open(args.url_file, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    if url and not url.startswith('#'):
                        urls.append(url)
            logger.info(f"파일에서 {len(urls)}개의 URL을 로드했습니다: {args.url_file}")
        except Exception as e:
            logger.error(f"URL 파일({args.url_file})을 읽는 중 오류가 발생했습니다: {e}")
            sys.exit(1)

    return args, config, urls
