import logging
from utils.config import setup_logger, parse_args_and_load_config
from crawler.manager import CrawlerManager

# 로거 설정
setup_logger()
logger = logging.getLogger("crawler_main")

def main():
    args, config, urls = parse_args_and_load_config()

    logger.info("웹 크롤러 작업 시작...")
    
    manager = CrawlerManager(config, args)
    manager.run(urls)

if __name__ == "__main__":
    main()

