from bs4 import BeautifulSoup
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class CSSParser:
    def parse(self, html: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        rules 예시:
        {
            "title": {"selector": "h1.article-title", "type": "css"},
            "body": {"selector": "div.content p", "type": "css", "multiple": True}
        }
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = {}
        
        for field, rule in rules.items():
            rule_type = rule.get('type', 'css')
            if rule_type != 'css':
                continue # css 파서가 처리할 대상이 아니면 건너뜀
            
            selector = rule.get('selector')
            if not selector:
                continue
                
            multiple = rule.get('multiple', False)
            
            try:
                if multiple:
                    elements = soup.select(selector)
                    result[field] = [el.get_text(strip=True) for el in elements] if elements else None
                else:
                    element = soup.select_one(selector)
                    result[field] = element.get_text(strip=True) if element else None
            except Exception as e:
                logger.warning(f"Failed to parse field '{field}' with selector '{selector}': {e}")
                result[field] = None
                
        return result
