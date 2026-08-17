# Stock Price & Technical Analysis Dashboard

This is an interactive web dashboard built using Python, Dash, and Plotly which displays stock price through candlestick charts alongside technical indicators (SMA, RSI) for any ticker symbol.

## Features
- Live stock data via Yahoo Finance (yfinance)
- Interactive candlestick chart with 20-day and 50-day moving averages
- RSI subplot with overbought/oversold reference lines
- Custom date range selection
- Error handling for invalid ticker symbols

## Tech Stack
- Python
- Dash / Plotly
- pandas
- yfinance
- ta (technical analysis library)

## How to run
1. Clone this repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python app.py`
6. Open `http://127.0.0.1:8050` in your browser