import feedparser
from config import Config

class NewsCollector:
    def __init__(self):
        self.rss_sources = Config.GLOBAL_NEWS_RSS
        
    def fetch_rss_news(self):
        """
        Config에 등록된 RSS 피드를 순회하며 뉴스 수집
        """
        news_items = []
        for source_name, url in self.rss_sources.items():
            try:
                # 타임아웃 설정을 위해 feedparser의 agent 조절이 필요할 수 있으나 기본 사용
                feed = feedparser.parse(url)
                
                # 각 매체별 최신 3개 기사만 가져오기 (API 호출 비용 절약 및 속도)
                for entry in feed.entries[:3]: 
                    news_items.append({
                        "source": source_name,
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.get("published", "Unknown"),
                        # 요약이 없으면 제목으로 대체, 너무 길면 자름
                        "summary": entry.get("summary", entry.title)[:300] 
                    })
            except Exception as e:
                print(f"⚠️ RSS Load Error ({source_name}): {e}")
                
        return news_items

    def get_all_news(self):
        # 레딧 함수 호출 제거 -> 오직 RSS 뉴스만 반환
        return self.fetch_rss_news()

if __name__ == "__main__":
    # 테스트용
    collector = NewsCollector()
    news = collector.get_all_news()
    print(f"수집된 뉴스 개수: {len(news)}")
    if news:
        print(news[0])