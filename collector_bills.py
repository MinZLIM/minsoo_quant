import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from config import Config

class BillCollector:
    def __init__(self):
        # 대한민국 국회 의안정보시스템 Open API URL (예시)
        # 실제 사용 시: https://open.assembly.go.kr/portal/data/service/selectServicePage.do/INF000000001
        self.base_url = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11" 

    def fetch_recent_bills(self):
        """
        최근 발의/가결된 법안 정보를 가져옵니다.
        API 키가 없으면 빈 리스트를 반환하거나 샘플 데이터를 반환하도록 예외 처리.
        """
        bills = []
        try:
            # 실제 API 호출 로직 (API 키 필요)
            params = {
                'KEY': Config.DATA_API_KEY,
                'Type': 'json',
                'pIndex': 1,
                'pSize': 5,
                'AGE': '22' # 22대 국회
            }
            # response = requests.get(self.base_url, params=params)
            # data = response.json()
            # 여기서 데이터 파싱 로직 구현
            
            # --- [시뮬레이션 데이터] 실제 API 연동 전 테스트용 ---
            bills.append({
                "title": "반도체 산업 지원을 위한 조세특례제한법 개정안",
                "status": "본회의 가결",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "반도체 시설 투자에 대한 세액 공제 비율을 확대하는 내용 포함."
            })
            bills.append({
                "title": "디지털 헬스케어 진흥법",
                "status": "위원회 심사",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "비대면 진료 및 의료 데이터 활용 규제 완화."
            })
            # --------------------------------------------------
            
        except Exception as e:
            print(f"Error fetching bills: {e}")
            
        return bills

if __name__ == "__main__":
    collector = BillCollector()
    print(collector.fetch_recent_bills())