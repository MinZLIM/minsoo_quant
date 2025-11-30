import google.generativeai as genai
import json
from config import Config

class StockAnalyzer:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_content(self, data_list):
        results = []
        
        # 사용자가 제공한 전문 투자 로직 (System Instruction)
        investment_logic = """
        너는 '이벤트 드리븐 전략'을 구사하는 최상위 헤지펀드 매니저야. 
        아래 [업종별 핵심 키워드]와 [투자 판단 로직]을 기준으로 뉴스를 분석해.

        [업종별 핵심 키워드 및 재료]
        1. 반도체/IT: 벤더 진입(엔비디아/삼성), 수율 안정, 신기술(HBM/CXL/유리기판), D램 가격 반등.
        2. 2차전지/EV: 대규모 수주(조 단위), 공장 착공(CAPEX), IRA/AMPC 정책 수혜, 전고체/실리콘음극재.
        3. 엔터/게임: 사전예약 대박, 판호 발급(중국), 웹툰 IP 드라마화.
        4. 건설/조선: 우크라이나/네옴시티 재건, SCFI/신조선가 상승, 원자재 가격 하락.
        5. 금융/지주: 자사주 소각, 밸류업 공시, 금리 인상기, 경영권 분쟁.
        6. 소비재(화장품/의류): 비중국 수출 급증, 유커/단체관광 허용.

        [★매우 중요: 투자 판단 로직 (재료의 성격 구분)]
        주식 시장 격언: "소문에 사서 뉴스에 팔라 (Buy the rumor, sell the news)"
        
        - **기대감(Expectation) -> 진입(Buy) 시그널**: 
          결과가 나오기 전 기대감이 형성되는 단계.
          (예: 임상 3상 '진입', 공장 착공 '예정', 신작 출시 '임박', 수주 '협상 중')
          
        - **재료 소멸(Realization) -> 주의/매도(Caution) 시그널**:
          기다리던 결과가 확정되어 뉴스로 나온 단계. 단기 차익 실현 매물이 나올 수 있음.
          (예: FDA 승인 '완료', 실적 '발표', 신작 '출시', 계약 '체결'(이미 알려진 경우))
        """

        for item in data_list:
            prompt = f"""
            {investment_logic}
            
            [분석 대상 뉴스/법안]
            제목: {item.get('title')}
            내용: {item.get('summary', item.get('content', ''))}
            출처: {item.get('source', 'Unknown')}
            
            위 내용을 분석하여 아래 JSON 형식으로만 응답해. 설명은 필요 없음.
            
            {{
                "sector": "위 6대 업종 중 하나 (해당 없으면 '기타')",
                "detected_keyword": "본문에서 발견된 핵심 단어 (예: HBM, 판호 발급)",
                "market_phase": "Expectation" 또는 "Realization",
                "investment_signal": "Strong Buy" 또는 "Buy" 또는 "Caution(Sell the news)" 또는 "Neutral",
                "related_stocks": ["종목명1", "종목명2"],
                "reasoning": "왜 이 페이즈(기대감/소멸)로 판단했는지, 어떤 종목이 왜 수혜인지 1문장 요약"
            }}
            """
            
            try:
                response = self.model.generate_content(prompt)
                text_response = response.text.replace('```json', '').replace('```', '').strip()
                analysis = json.loads(text_response)
                
                # 중요도 필터링을 위해 점수 로직 간단 추가 (Buy면 높은 점수)
                score = 8 if "Buy" in analysis['investment_signal'] else 4
                if analysis['investment_signal'] == "Caution(Sell the news)":
                    score = 6 # 재료 소멸도 중요 정보이므로

                merged_data = {**item, **analysis, "importance_score": score}
                results.append(merged_data)
                
            except Exception as e:
                print(f"❌ Analysis failed for {item.get('title')}: {e}")
                results.append({**item, "importance_score": 0, "reasoning": "분석 실패"})
                
        return results