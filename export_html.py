import json
import yfinance as yf
import pandas as pd
from datetime import datetime

def export_standalone_html(output_file='qqq_monthly_chart.html'):
    print("Fetching QQQ unadjusted monthly data from Yahoo Finance...")
    ticker = yf.Ticker('QQQ')
    df = ticker.history(period='max', interval='1mo', auto_adjust=False).reset_index()
    
    df['time'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    df['ma60'] = df['Close'].rolling(window=60).mean()
    
    candles = []
    ma60_line = []
    stats = []
    
    for _, row in df.iterrows():
        t = row['time']
        o = round(float(row['Open']), 2)
        h = round(float(row['High']), 2)
        l = round(float(row['Low']), 2)
        c = round(float(row['Close']), 2)
        v = int(row.get('Volume', 0)) if not pd.isna(row.get('Volume', 0)) else 0
        
        candles.append({'time': t, 'open': o, 'high': h, 'low': l, 'close': c, 'volume': v})
        
        ma_val = None
        diff_val = None
        growth_pct = None  # (Close / MA60 - 1) * 100
        
        if not pd.isna(row['ma60']):
            ma_val = round(float(row['ma60']), 2)
            diff_val = round(c - ma_val, 2)
            growth_pct = round(((c / ma_val) - 1.0) * 100.0, 2)
            
            ma60_line.append({'time': t, 'value': ma_val})
        
        stats.append({
            'time': t,
            'open': o,
            'high': h,
            'low': l,
            'close': c,
            'ma60': ma_val,
            'diff': diff_val,
            'growth_pct': growth_pct
        })
        
    dataset = {
        'ticker': 'QQQ',
        'name': 'Invesco QQQ Trust (Monthly)',
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'candles': candles,
        'ma60': ma60_line,
        'stats': stats,
        'count': len(candles)
    }
    
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    inject_script = f"""
    <script>
        const EMBEDDED_DATA = {json.dumps(dataset)};
        async function reloadData(force = false) {{
            if (force) {{
                try {{
                    const res = await fetch(`/api/data?force=true`);
                    const json = await res.json();
                    if (json.status === 'success') {{
                        renderData(json.data);
                        return;
                    }}
                }} catch (e) {{}}
            }}
            renderData(EMBEDDED_DATA);
            document.getElementById('loading').style.display = 'none';
        }}
    </script>
    """
    
    html = html.replace('</body>', f'{inject_script}\n</body>')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Successfully generated standalone HTML: {output_file}")

if __name__ == '__main__':
    export_standalone_html()
