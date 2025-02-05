import yfinance as yf
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_stock_details(symbol):
    stock_data = {}

    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info

        stock_data["current_price"] = stock_info.get("currentPrice", "N/A")
        stock_data["high"] = stock_info.get("dayHigh", "N/A")
        stock_data["low"] = stock_info.get("dayLow", "N/A")
        stock_data["name"] = stock_info.get("longName", "N/A")
        stock_data["market_cap"] = stock_info.get("marketCap", "N/A")
        stock_data["pe_ratio"] = stock_info.get("trailingPE", "N/A")
        stock_data["peg_ratio"] = stock_info.get("pegRatio", "N/A")
        stock_data["eps"] = stock_info.get("trailingEps", "N/A")

    except Exception as e:
        print(f"Error fetching stock data: {e}")

    return stock_data

@app.route("/api/historical/<symbol>")
def get_historical_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d", interval="5m")  # Fetch 1-day data (5-minute intervals)
        
        # Convert data to JSON format
        historical_data = [
            {"time": date.strftime('%H:%M'), "close": row["Close"]}
            for date, row in hist.iterrows()
        ]

        print(f"Fetched Data for {symbol}: {historical_data}")  # Debugging Output
        return jsonify(historical_data)
    
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return jsonify([])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        symbol = request.form.get("symbol", "").upper()
        if symbol:
            return render_template("result.html", stock_info=get_stock_details(symbol), symbol=symbol)
    
    return render_template("index.html")

@app.route("/api/historical/<symbol>")
def historical_api(symbol):
    return jsonify(get_historical_data(symbol))

if __name__ == "__main__":
    app.run(debug=True)
