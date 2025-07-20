import yfinance as yf
import plotly.graph_objects as go
def get_stock_data(ticker_symbol: str):

    stock = yf.Ticker(ticker_symbol)
    hist = stock.history(period="1y")
    if hist.empty:
        print(f"No data found for ticker: {ticker_symbol}")
        return None, None
    fig = go.Figure(data=go.Scatter(
        x=hist.index,
        y=hist['Close'],
        mode='lines',
        name='Close'
    ))

    fig.update_layout(
        title_text=f"{stock.info.get('longName', ticker_symbol)} - Price Trend",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        template="plotly_white"
    )
    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return stock.info, chart_html