import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 1. Google Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # 2. 공공데이터 포털 (국회 의안정보)
    DATA_API_KEY = os.getenv("DATA_GO_KR_API_KEY")

    # 3. 뉴스 RSS 피드 (국내/해외 주요 매체)
    # 필요에 따라 매체 URL을 추가/삭제하세요.
    GLOBAL_NEWS_RSS = {
        # 한국 경제 관련 구글 뉴스 (가장 속보성이 좋음)
        "Google_News_Economy_KR": "https://news.google.com/rss/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNR2RtY0hNekVnSmxiaWdBUAE?hl=ko&gl=KR&ceid=KR%3Ako",
        
        # 주요 언론사 RSS 예시 (실제 작동하는 URL로 관리 필요)
        "MK_Economy": "https://www.mk.co.kr/rss/30000001/", # 매일경제 경제
        "Hankyung_Stock": "https://www.hankyung.com/feed/stock", # 한국경제 증권
        
        # 해외 거시 경제 (WSJ, Bloomberg 등은 유료라 구글 영문 뉴스로 대체 추천)
        "Google_Finance_US": "https://news.google.com/rss/search?q=US+Economy+Interest+Rate&hl=en-US&gl=US&ceid=US:en"
    }