import google.generativeai as genai
import json
from config import Config

class StockAnalyzer:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        # 사용자 환경에 맞는 최신 모델 (속도+지능 밸런스)
        self.model = genai.GenerativeModel('gemini-2.5-flash') 

    def analyze_content(self, data_list):
        results = []
        
        # 1. 업종별 핵심 재료 (지식 주입)
        sector_knowledge = """
        [업종별 핵심 키워드 및 재료 가이드]
        1. 반도체/IT: 벤더 진입(엔비디아/삼성), 수율 안정, HBM/CXL/유리기판, D램 가격 반등.
        2. 2차전지/EV: 대규모 수주(조 단위), 공장 착공, IRA/AMPC 정책 수혜, 전고체 배터리.
        3. 엔터/게임/콘텐츠: 사전예약 흥행, 판호 발급(중국), 웹툰 IP 드라마화, 글로벌 차트 진입.
        4. 건설/조선/기계: 우크라이나/네옴시티 재건, SCFI/신조선가 상승, 원자재 가격 하락.
        5. 바이오/제약: FDA 승인, 기술수출(L/O), 임상 3상 진입.
        6. 금융/지주: 자사주 소각, 밸류업 공시, 금리 인상(예대마진).
        """

        # 2. 투자 판단 로직 (격언 적용)
        investment_logic = """
        [투자 판단 로직: "소문에 사서 뉴스에 팔라 (Buy the rumor, sell the news)"]
        - **기대감(Expectation) -> 매수(Buy)**: 결과가 나오기 전 기대감이 형성되는 단계.
          (예: 임상 '진입', 공장 착공 '예정', 신작 출시 '임박', 수주 '협상 중')
          
        - **재료 소멸(Realization) -> 주의/관망(Caution)**: 기다리던 결과가 뉴스로 확정된 단계.
          (예: FDA '승인 완료', 실적 '발표', 신작 '출시', 계약 '체결')
          단, '어닝 서프라이즈'나 '예상을 뛰어넘는 초대형 수주'는 예외적으로 추가 상승 가능.
        """

        # 3. 출력 요구사항 (매매가 포함)
        output_requirements = """
        위 [지식]과 [로직]을 바탕으로 뉴스를 분석해.
        
        [요청 사항]
        1. 뉴스를 한글 1줄로 요약할 것.
        2. 해당 재료가 '기대감'인지 '재료 소멸'인지 판단하여 신호를 줄 것.
        3. 관련주를 선정하고, 구체적인 실전 매매 전략(진입/익절/손절)을 수립할 것.
        4. 가격은 현재가를 모르므로 '시초가', '눌림목', '5일선', '전고점', '퍼센트(%)' 등을 활용하여 구체적으로 제시할 것.
        
        [출력 JSON 포맷]
        {
            "summary_1line": "핵심 내용 1줄 요약",
            "investment_signal": "Buy(기대감)" 또는 "Caution(재료소멸)" 또는 "Neutral",
            "sector": "업종명 (예: 반도체)",
            "related_stocks": [
                {
                    "name": "종목명",
                    "reason": "선정 이유 짧게",
                    "strategy": {
                        "buy": "진입가 가이드 (예: 시초가 이하 분할 매수, -3% 눌림목)",
                        "target": "익절가 가이드 (예: +10% 슈팅 시, 전고점 돌파 시)",
                        "stop_loss": "손절가 가이드 (예: 20일선 이탈 시, -5% 손절)"
                    }
                }
            ]
        }
        """

        for item in data_list:
            prompt = f"""
            너는 20년 경력의 이벤트 드리븐 전략 전문 펀드매니저야.
            
            {sector_knowledge}
            {investment_logic}
            {output_requirements}
            
            [분석할 뉴스]
            제목: {item.get('title')}
            내용: {item.get('summary', item.get('content', ''))}
            출처: {item.get('source', 'Unknown')}
            
            위 정보를 바탕으로 오직 JSON 포맷의 데이터만 출력해. (마크다운 코드 블록 제외)
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                # JSON 파싱 (마크다운 제거)
                text_response = response.text.replace('```json', '').replace('```', '').strip()
                analysis = json.loads(text_response)
                
                # 원본 데이터와 분석 결과 병합
                merged_data = {**item, **analysis}
                results.append(merged_data)
                
            except Exception as e:
                print(f"❌ Analysis failed for {item.get('title')}: {e}")
                # 에러 발생 시 기본값 채워서 반환
                results.append({
                    **item, 
                    "summary_1line": "분석 실패", 
                    "investment_signal": "Error", 
                    "related_stocks": []
                })
                
        return results