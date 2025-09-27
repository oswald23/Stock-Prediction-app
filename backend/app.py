
from flask import Flask, request, jsonify
from flask_cors import CORS
from openbb_terminal.sdk import openbb
from prophet import Prophet
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/forecast', methods=['GET'])
def forecast():
    ticker = request.args.get('ticker', '').upper().strip()
    if not ticker:
        return jsonify({'error': 'Ticker parameter is required'}), 400
    try:
        # Fetch historical daily prices (YahooFinance by default)
        df = openbb.stocks.load(symbol=ticker, interval=1440, start_date="2020-01-01", source="YahooFinance")
        if df is None or df.empty:
            return jsonify({'error': f'No data found for ticker {ticker}'}), 404

        # Prepare dataframe for Prophet
        df = df.copy()
        df.index = pd.to_datetime(df.index)
        price_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
        data = df[[price_col]].reset_index()
        data.columns = ['ds', 'y']  # Prophet expects 'ds' and 'y'

        # Train Prophet model
        model = Prophet()
        model.fit(data)

        # Forecast next 30 days
        future = model.make_future_dataframe(periods=30, freq='D', include_history=False)
        forecast = model.predict(future)

        results = []
        for _, row in forecast.iterrows():
            results.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'price': round(float(row['yhat']), 2)
            })

        return jsonify({'ticker': ticker, 'forecast': results})

    except Exception as e:
        print('Forecast error:', e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
