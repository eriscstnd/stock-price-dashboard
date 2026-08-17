import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import ta

app = dash.Dash(__name__)

app.layout = html.Div(style={"fontFamily": "Arial", "margin": "40px"}, children=[
    html.H1("Stock Price & Technical Analysis Dashboard", style={"textAlign": "center"}),

    html.Div(style={"display": "flex", "justifyContent": "center", "gap": "20px", "marginBottom": "20px"}, children=[
        dcc.Input(id="ticker-input", value="AAPL", type="text", style={"padding": "8px", "fontSize": "16px"}),
        dcc.DatePickerRange(
            id="date-range",
            start_date="2025-01-01",
            end_date="2026-08-18",
        ),
    ]),

    html.Div(id="error-message", style={"textAlign": "center", "color": "red", "fontWeight": "bold"}),

    dcc.Graph(id="price-chart"),
])


@app.callback(
    Output("price-chart", "figure"),
    Output("error-message", "children"),
    Input("ticker-input", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_chart(ticker, start_date, end_date):
    try:
        df = yf.download(ticker, start=start_date, end=end_date)

        if df.empty:
            return go.Figure(), f"No data found for ticker '{ticker}'. Please check the symbol."

        df.columns = df.columns.get_level_values(0)  # same fix as before

        df["SMA_20"] = ta.trend.sma_indicator(df["Close"], window=20)
        df["SMA_50"] = ta.trend.sma_indicator(df["Close"], window=50)
        df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.7, 0.3],
            vertical_spacing=0.05,
            subplot_titles=(f"{ticker.upper()} Price", "RSI (14)")
        )

        fig.add_trace(go.Candlestick(
            x=df.index, open=df["Open"], high=df["High"],
            low=df["Low"], close=df["Close"], name="Price"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"], line=dict(color="orange", width=1.5), name="SMA 20"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], line=dict(color="blue", width=1.5), name="SMA 50"), row=1, col=1)

        fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], line=dict(color="purple", width=1.5), name="RSI"), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        fig.update_layout(
            height=700,
            xaxis_rangeslider_visible=False,
            template="plotly_white",
        )

        return fig, ""

    except Exception as e:
        return go.Figure(), f"Error fetching data: {e}"


if __name__ == "__main__":
    app.run(debug=True)