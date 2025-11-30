import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import Config

def create_html_report(results):
    """
    분석 결과를 이메일용 HTML로 변환
    """
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #2c3e50;">🚀 AI 증시 전략 리포트 ({datetime.now().strftime('%Y-%m-%d')})</h2>
        <hr>
    """
    
    for item in results:
        signal = item.get('investment_signal', 'Neutral')
        
        # 신호별 색상 및 아이콘 지정
        color = "#95a5a6" # 회색 (Neutral)
        icon = "⚪"
        if "Buy" in signal: 
            color = "#e74c3c" # 빨간색 (매수)
            icon = "🔥"
        elif "Caution" in signal: 
            color = "#2980b9" # 파란색 (주의)
            icon = "⚠️"
            
        # 전략 텍스트 구성
        stocks_html = ""
        for stock in item.get('related_stocks', []):
            strategy = stock.get('strategy', {})
            # 전략이 딕셔너리가 아닐 경우 대비
            if not isinstance(strategy, dict):
                strategy = {}
                
            stocks_html += f"""
            <li style="margin-bottom: 5px;">
                <b>{stock.get('name', '종목명')}</b><br>
                <span style="font-size: 0.9em; color: #555;">
                - 진입: {strategy.get('buy', '-')}<br>
                - 익절: {strategy.get('target', '-')}<br>
                - 손절: {strategy.get('stop_loss', '-')}
                </span>
            </li>
            """
            
        # 카드 HTML 조립
        html_body += f"""
        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 8px; border-left: 5px solid {color};">
            <h3 style="margin-top: 0; color: #333;">
                <a href="{item.get('link', '#')}" style="text-decoration: none; color: #333;">{icon} {item.get('title', '제목 없음')}</a>
            </h3>
            <p style="font-size: 0.9em; color: #666;">📅 {item.get('published', '')} | 📂 {item.get('sector', '기타')}</p>
            <p style="background-color: #f9f9f9; padding: 10px; border-radius: 5px;">
                <b>요약:</b> {item.get('summary_1line', '요약 없음')}
            </p>
            <p><b>📊 전략 ({signal}):</b></p>
            <ul>{stocks_html}</ul>
            <div style="text-align: right;">
                <a href="{item.get('link', '#')}" style="background-color: {color}; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px; font-size: 0.9em;">
                    기사 원문 보기 >
                </a>
            </div>
        </div>
        """
        
    html_body += """
        <hr>
        <p style="font-size: 0.8em; color: #999; text-align: center;">
            본 리포트는 AI 분석 결과이며 투자 권유가 아닙니다.
        </p>
    </body>
    </html>
    """
    return html_body

def send_email_report(results):
    if not results:
        print("전송할 내용이 없습니다.")
        return

    try:
        # 이메일 객체 생성
        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL_SENDER
        msg['To'] = Config.EMAIL_RECEIVER
        msg['Subject'] = f"[{datetime.now().strftime('%m/%d')}] 📈 AI 증시 전략 리포트 도착"

        # HTML 본문 추가
        html_content = create_html_report(results)
        msg.attach(MIMEText(html_content, 'html'))

        # SMTP 서버 연결 및 전송 (Gmail 기준)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # 보안 연결
        server.login(Config.EMAIL_SENDER, Config.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"📧 이메일 전송 성공! ({Config.EMAIL_RECEIVER})")
        
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")

# 테스트용 실행 코드
if __name__ == "__main__":
    test_data = [{
        "title": "테스트 뉴스: 삼성전자 HBM 공급 확정",
        "link": "https://naver.com",
        "published": "2024-05-20",
        "investment_signal": "Buy",
        "summary_1line": "삼성전자가 엔비디아에 HBM3E 공급을 시작한다는 소식",
        "related_stocks": [{"name": "삼성전자", "strategy": {"buy": "시초가", "target": "10만전자", "stop_loss": "7만붕괴"}}]
    }]
    print("테스트 메일 발송 시도...")
    send_email_report(test_data)