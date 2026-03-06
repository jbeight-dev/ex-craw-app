import re
from urllib.parse import urlparse

def get_filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    filename = parsed.netloc + parsed.path.replace('/', '_')
    if not filename or filename == '_':
        filename = "index"
    return filename

def sanitize_filename(name: str) -> str:
    if not name:
        return "no_title"
    # 파일명으로 사용할 수 없는 문자 제거
    s = re.sub(r'[\\/*?:"<>|]', "", str(name))
    s = re.sub(r'\s+', "_", s)
    return s.strip('_')[:50]  # 너무 길어지지 않게 50자로 제한
