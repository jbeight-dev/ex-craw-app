import logging
import json
from datetime import datetime
from typing import List, Dict, Any

from crawler.static import StaticCrawler
from crawler.dynamic import DynamicCrawler
from parser.css_parser import CSSParser
from parser.xpath_parser import XPathParser
from storage.json_writer import JsonWriter
from storage.csv_writer import CsvWriter
from storage.raw_html_writer import RawHtmlWriter
from utils.helpers import get_filename_from_url, sanitize_filename

logger = logging.getLogger("crawler_manager")

class CrawlerManager:
    def __init__(self, config: Dict[str, Any], args: Any):
        self.config = config
        self.args = args
        self.target_config = config.get("target", {})
        self.extract_config = config.get("extract", {})
        self.output_config = config.get("output", {})
        
        self.timeout = self.target_config.get("timeout", 10.0)
        self.retry_count = self.target_config.get("retry_count", 3)
        self.delay = args.delay if args.delay is not None else self.target_config.get("delay_seconds", 1.0)
        
        use_js = args.render_js or self.target_config.get("render_js", False)
        
        if use_js:
            self.crawler = DynamicCrawler()
            logger.info("자바스크립트 렌더링 지원 크롤러(Playwright)로 설정되었습니다.")
        else:
            self.crawler = StaticCrawler()
            logger.info("정적 크롤러(requests)로 설정되었습니다.")
            
        # Parser 초기화
        self.css_parser = CSSParser()
        self.xpath_parser = XPathParser()
        
        # Storage 모듈 초기화
        self.json_writer = JsonWriter()
        self.csv_writer = CsvWriter()
        self.raw_html_writer = RawHtmlWriter()

    def run(self, urls: List[str]) -> List[Dict[str, Any]]:
        results = []
        today_str = datetime.now().strftime("%Y-%m-%d")

        for url in urls:
            logger.info(f"크롤링 시작: {url}")
            html_code = self.crawler.fetch(url, timeout=self.timeout, retry_count=self.retry_count, delay=self.delay)
            
            if html_code:
                # 파싱
                parsed_data = {}
                css_result = self.css_parser.parse(html_code, self.extract_config)
                xpath_result = self.xpath_parser.parse(html_code, self.extract_config)
                
                parsed_data.update(css_result)
                parsed_data.update(xpath_result)
                
                parsed_data["url"] = url
                parsed_data["crawled_at"] = datetime.now().isoformat()
                
                results.append(parsed_data)
                logger.info("데이터 추출 완료")
                
                address_str = get_filename_from_url(url)
                
                raw_title = parsed_data.get("title")
                if isinstance(raw_title, list):
                    raw_title = raw_title[0] if raw_title else "no_title"
                title_str = sanitize_filename(raw_title)
                
                raw_path = f"./output/raw/{today_str}/raw_{address_str}_{title_str}.html"
                self.raw_html_writer.save(html_code, raw_path)
                
                output_format = self.args.output or self.output_config.get("format", "json")
                if output_format == "json":
                    processed_path = f"./output/processed/{address_str}_{title_str}.json"
                    self.json_writer.save(parsed_data, processed_path)
                elif output_format == "csv":
                    processed_path = f"./output/processed/{address_str}_{title_str}.csv"
                    self.csv_writer.save(parsed_data, processed_path)
                else:
                    logger.warning(f"지원되지 않는 출력 형식입니다: {output_format}")

            else:
                logger.warning(f"HTML을 가져오지 못해 추출을 건너뜁니다: {url}")

        if self.args.stdout:
            print(json.dumps(results, ensure_ascii=False, indent=2))

        logger.info("크롤링 작업 완료")
        return results
