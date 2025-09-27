from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
from prophet import Prophet
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/forecast', methods=['GET'])
def forecast():
    ticker = (request.args.get("ticker") or "").upper().strip()
    if not ticker:
        return jsonify({"error": "Ticker parameter is required"}), 400
    try:
        # Download daily stock data from Yahoo Finance
        df = yf.download(ticker, start="2020-01-01", progress=False)
        if df.empty:
            return jsonify({"error": f"No data found for ticker {ticker}"}), 404

        # Prepare data for Prophet
        df = df.reset_index()
        df = df.rename(columns={"Date": "ds", "Adj Close": "y"})
        if "y" not in df.columns or df["y"].isna().all():
            df = df.rename(columns={"Close": "y"})
        df = df[["ds", "y"]].dropna()

        # Forecast with Prophet
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=30, freq="D", include_history=False)
        forecast = model.predict(future)

        results = [
            {"date": row["ds"].strftime("%Y-%m-%d"), "price": round(float(row["yhat"]), 2)}
            for _, row in forecast.iterrows()
        ]
        return jsonify({"ticker": ticker, "forecast": results})

    except Exception as e:
        print("Forecast error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
