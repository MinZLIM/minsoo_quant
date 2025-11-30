import time
from collector_bills import BillCollector
from collector_news import NewsCollector
from analyzer import StockAnalyzer

def print_simple_card(data):
    # 신호에 따른 이모지
    signal = data.get('investment_signal', 'Neutral')
    icon = "⚪"
    if "Buy" in signal: icon = "🔥 [매수 기회]"
    elif "Caution" in signal: icon = "⚠️ [관망/주의]"

    print(f"\n{'-'*30}")
    print(f"{icon} {data.get('title')}")
    print(f"{'-'*30}")
    
    # 1. 발행 정보 (일시 & URL)
    print(f"📅 일시: {data.get('published', '날짜 정보 없음')}")
    print(f"🔗 링크: {data.get('link', 'URL 없음')}")
    print(f"📝 요약: {data.get('summary_1line', '요약 없음')}")
    
    print(f"\n💰 [추천 종목 및 전략]")
    stocks = data.get('related_stocks', [])
    
    if not stocks:
        print("   -> 뚜렷한 관련주 없음")
    
    for stock in stocks:
        name = stock.get('name', '종목명')
        strat = stock.get('strategy', {})
        
        print(f"   📌 {name}")
        print(f"      🔵 매수: {strat.get('buy', '-')}")
        print(f"      🔴 익절: {strat.get('target', '-')}")
        print(f"      🛡️ 손절: {strat.get('stop_loss', '-')}")
    
    print("="*30 + "\n")

def job():
    print("🚀 [증시 알리미] 뉴스 수집 및 매매 전략 분석 중...\n")
    
    # 1. 수집
    # collector_news.py가 feedparser로 잘 동작한다고 가정
    news_collector = NewsCollector()
    news_data = news_collector.get_all_news()
    
    # 데이터가 너무 많으면 테스트용으로 5개만 자름
    if len(news_data) > 5:
        news_data = news_data[:5]

    if not news_data:
        print("📭 분석할 새로운 뉴스가 없습니다.")
        return

    # 2. 분석
    analyzer = StockAnalyzer()
    analyzed_results = analyzer.analyze_content(news_data)
    
    # 3. 리포팅
    print(f"📊 총 {len(analyzed_results)}건의 분석 리포트")
    for res in analyzed_results:
        print_simple_card(res)

if __name__ == "__main__":
    job()