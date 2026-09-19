# QQQ Monthly 60MA Disparity Mobile Chart (QQQ 월봉 60선 이격도 분석 차트)

> QQQ(Invesco QQQ Trust)의 월봉(Monthly Candlestick) 및 60월 이동평균선(60-Month Moving Average)을 실시간으로 수집하고, 각 월봉 클릭/터치 시 60선과의 주가 차이 및 이격률(%)을 분석할 수 있는 모바일 최적화 전문가용 차트 애플리케이션입니다.

---

## 🌟 주요 기능

1. **실시간/최신 QQQ 월봉 데이터 로딩**: Yahoo Finance API(`yfinance`)를 통해 상장 이후 전체 월봉 캔들 데이터 수집.
2. **60월 이동평균선(60MA) 단일 표시**: 장기 추세 지표인 60월 SMA 오버레이.
3. **인터랙티브 이격도 분석 UI**:
   - 차트의 특정 월봉을 클릭하거나 터치(모바일 드래그/탭)하면 상단 대시보드에 실시간 지표 표시.
   - **종가 대비 60선 차이율 (%)**: `((Close - MA60) / Close) * 100%`
   - **60선 대비 괴리율 (%)**: `((Close - MA60) / MA60) * 100%`
   - **주가 차이 ($)**: `Close - MA60`
   - 시가(Open), 고가(High), 저가(Low), 종가(Close), 60MA 가격 상세 제공.
4. **TradingView Lightweight Charts v4 탑재**:
   - 금융 전문가용 다크 테마.
   - 모바일 제스처 최적화 (핀치 줌, 스크롤, 탭).
5. **독립 실행(Standalone HTML) 지원**: 서버 없이 단일 HTML 파일로 브라우저에서 바로 확인 가능.

---

## 🚀 빠른 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 웹 서버 실행 (모바일 / PC 브라우저 접속)
```bash
python app.py
```
- 브라우저에서 `http://localhost:5000` 접속.
- 동일 Wi-Fi 네트워크에 연결된 스마트폰의 경우 `http://[PC_내부_IP]:5000`으로 접속하여 모바일 화면으로 확인 가능.

### 3. 단일 정적 HTML 파일 생성 (선택 사항)
웹 서버 없이 파일만으로 브라우저에서 열고 싶을 때:
```bash
python export_html.py
```
- `qqq_monthly_chart.html` 파일이 생성되며 더블클릭으로 바로 열람 가능.

---

## 📂 프로젝트 구조
- `app.py`: Flask 기반 데이터 수집 백엔드 및 실시간 API 서버
- `export_html.py`: 오프라인용 정적 HTML 생성 스크립트
- `templates/index.html`: TradingView Lightweight Charts 기반 모바일 반응형 프론트엔드
- `requirements.txt`: 프로젝트 필수 라이브러리 목록
- `qqq_monthly_chart.html`: 생성된 정적 차트 파일
