from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

app = Flask(__name__)

_cache_data = None
_cache_time = 0
CACHE_DURATION_SEC = 60

def fetch_qqq_monthly_data(force=False):
    global _cache_data, _cache_time
    now = time.time()
    
    if not force and _cache_data is not None and (now - _cache_time) < CACHE_DURATION_SEC:
        return _cache_data
    
    try:
        ticker = yf.Ticker('QQQ')
        df = ticker.history(period='max', interval='1mo', auto_adjust=False)
        
        if df.empty:
            if _cache_data is not None:
                return _cache_data
            raise ValueError('No data fetched from Yahoo Finance')
            
        df = df.reset_index()
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
            
            candles.append({
                'time': t,
                'open': o,
                'high': h,
                'low': l,
                'close': c,
                'volume': v
            })
            
            ma_val = None
            diff_val = None
            growth_pct = None  # (Close / MA60 - 1) * 100
            
            if not pd.isna(row['ma60']):
                ma_val = round(float(row['ma60']), 2)
                diff_val = round(c - ma_val, 2)
                growth_pct = round(((c / ma_val) - 1.0) * 100.0, 2)
                
                ma60_line.append({
                    'time': t,
                    'value': ma_val
                })
            
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
            
        result = {
            'ticker': 'QQQ',
            'name': 'Invesco QQQ Trust (Monthly)',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'candles': candles,
            'ma60': ma60_line,
            'stats': stats,
            'count': len(candles)
        }
        
        _cache_data = result
        _cache_time = now
        return result
        
    except Exception as e:
        if _cache_data is not None:
            return _cache_data
        raise e

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    force = request.args.get('force', 'false').lower() == 'true'
    try:
        data = fetch_qqq_monthly_data(force=force)
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print('Starting QQQ Monthly 60MA Mobile Chart Server on http://0.0.0.0:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)
