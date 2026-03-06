from lxml import html
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class XPathParser:
    def parse(self, html_content: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        rules 예시:
        {
            "date": {"selector": "//span[@class='date']/text()", "type": "xpath"},
            "links": {"selector": "//a/@href", "type": "xpath", "multiple": True}
        }
        """
        try:
            tree = html.fromstring(html_content)
        except Exception as e:
            logger.error(f"HTML 문자열 파싱 중 오류 발생: {e}")
            return {}

        result = {}
        
        for field, rule in rules.items():
            rule_type = rule.get('type', 'css')
            if rule_type != 'xpath':
                continue # xpath 파서가 처리할 대상이 아니면 건너뜀
            
            selector = rule.get('selector')
            if not selector:
                continue
                
            multiple = rule.get('multiple', False)
            
            try:
                elements = tree.xpath(selector)
                
                # lxml의 xpath 결과는 리스트로 반환됨
                if not elements:
                    result[field] = None
                    continue

                if multiple:
                    # 텍스트 노드나 속성(attribute)인 경우 문자열을 직접 반환, 요소인 경우 text_content() 사용
                    result[field] = [
                        el.strip() if isinstance(el, str) else el.text_content().strip() 
                        for el in elements
                    ]
                else:
                    first_el = elements[0]
                    result[field] = first_el.strip() if isinstance(first_el, str) else first_el.text_content().strip()
            except Exception as e:
                logger.warning(f"Failed to parse field '{field}' with xpath '{selector}': {e}")
                result[field] = None
                
        return result
