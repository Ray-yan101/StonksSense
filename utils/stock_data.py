import yfinance as yf
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

def get_stock_data(ticker_symbol: str):
    stock = yf.Ticker(ticker_symbol)
    hist = stock.history(period="1y")
    if hist.empty:
        print(f"No data found for ticker: {ticker_symbol}")
        return None, None, None

    closes = hist['Close'].reset_index()
    X = np.arange(len(closes)).reshape(-1, 1)
    y = closes['Close'].values

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(len(closes), len(closes) + 5).reshape(-1, 1)
    predicted_prices = model.predict(future_days)

    future_dates = pd.date_range(closes['Date'].iloc[-1] + pd.Timedelta(days=1), periods=5)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist['Close'],
        mode='lines',
        name='Close'
    ))
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=predicted_prices,
        mode='lines',
        name='5-Day Prediction',
        line=dict(dash='dot', color='orange')
    ))
    fig.update_layout(
        title_text=f"{stock.info.get('longName', ticker_symbol)} - Price Trend & 5-Day Prediction",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        template="plotly_white",
        height=420,
        width=650,
        margin=dict(l=50, r=50, t=60, b=60),
        xaxis=dict(tickangle=45)
    )

    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return stock.info, chart_html, list(predicted_prices)
