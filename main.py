import time
from collector_bills import BillCollector
from collector_news import NewsCollector
from analyzer import StockAnalyzer

def print_colored_report(result):
    signal = result.get('investment_signal', 'Neutral')
    phase = result.get('market_phase', 'Unknown')
    
    # 이모지 및 시그널 매핑
    icon = "⚪"
    if "Buy" in signal:
        icon = "🔥 [진입 추천]"
    elif "Caution" in signal:
        icon = "📉 [재료 소멸/주의]"
        
    print(f"\n{icon} {result['title']}")
    print(f"   📂 업종: {result.get('sector')} | 🗝️ 키워드: {result.get('detected_keyword')}")
    print(f"   🔄 국면: {phase} ({'기대감 형성 중' if phase == 'Expectation' else '결과 확정/재료 노출'})")
    print(f"   📊 관련주: {', '.join(result.get('related_stocks', []))}")
    print(f"   💡 전략: {result.get('reasoning')}")
    print("-" * 60)

def job():
    print("🚀 [증시 알리미 봇] Event-Driven 전략 분석 시작...")
    
    # 인스턴스
    bill_collector = BillCollector()
    news_collector = NewsCollector()
    analyzer = StockAnalyzer()
    
    # 데이터 수집 (샘플링)
    # 실제 운용 시에는 collector 내부 로직을 통해 더 많은 데이터를 가져오세요.
    raw_data = news_collector.get_all_news() + bill_collector.fetch_recent_bills()
    
    if not raw_data:
        print("수집된 데이터가 없습니다.")
        return

    print(f"🧠 {len(raw_data)}건의 데이터에 대해 '기대감 vs 소멸' 여부를 판별 중입니다...")
    analyzed_results = analyzer.analyze_content(raw_data)
    
    print("\n" + "="*60)
    print("📢 AI 투자 전략 리포트")
    print("="*60)
    
    # 결과 출력
    for res in analyzed_results:
        # 기타 업종이거나 중요도가 너무 낮으면 스킵
        if res.get('sector') == '기타' or res.get('importance_score', 0) < 4:
            continue
        print_colored_report(res)

if __name__ == "__main__":
    job()