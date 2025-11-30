import time
from collector_bills import BillCollector
from collector_news import NewsCollector
from analyzer import StockAnalyzer
from notifier_email import send_email_report # [수정됨] 이메일 모듈 임포트

def job():
    print("🚀 [증시 알리미] 작동 시작...\n")
    
    # 1. 수집
    news_collector = NewsCollector()
    news_data = news_collector.get_all_news()
    
    # 테스트용 슬라이싱 (실제 사용 시 제거 가능)
    if len(news_data) > 5: news_data = news_data[:5]

    if not news_data:
        print("📭 새로운 뉴스가 없습니다.")
        return

    # 2. 분석
    analyzer = StockAnalyzer()
    analyzed_results = analyzer.analyze_content(news_data)
    
    # [추가] 중요도가 낮거나(Neutral), 전략이 없는 건 제외하고 보낼지 결정
    # 여기서는 'Buy'나 'Caution' 신호가 있는 것만 필터링해서 보냄
    important_results = [
        res for res in analyzed_results 
        if "Buy" in res.get('investment_signal', '') or "Caution" in res.get('investment_signal', '')
    ]
    
    if not important_results:
        print("📉 특이사항(매수/주의 신호)이 없어 이메일을 보내지 않습니다.")
        return

    # 3. 이메일 전송 (한 번에 묶어서)
    print(f"📧 중요 리포트 {len(important_results)}건을 이메일로 전송합니다...")
    send_email_report(important_results)
    
    print("=== 완료 ===")

if __name__ == "__main__":
    job()