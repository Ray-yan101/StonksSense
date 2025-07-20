from flask import Flask, render_template, request
from utils.stock_data import get_stock_data
from utils.news_sentiment import analyze_sentiment
from config import NEWS_API_KEY

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    ticker = request.form.get("ticker", "").upper().strip()

    if not ticker:
        return render_template("index.html", error="Please enter a stock ticker.")

    stock_info, chart_html, predicted_prices = get_stock_data(ticker)

    
    if not stock_info:
        error_msg = f"Could not find data for '{ticker}'. Please try another symbol."
        return render_template("index.html", error=error_msg)

    sentiment, articles = analyze_sentiment(stock_info.get("longName"), NEWS_API_KEY)

    return render_template(
        "results.html",
        stock_info=stock_info,
        chart=chart_html,
        sentiment=sentiment,
        articles=articles,
        predicted_prices=predicted_prices 
    )

if __name__ == "__main__":
    app.run(debug=True)