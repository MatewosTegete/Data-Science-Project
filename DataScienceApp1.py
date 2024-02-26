import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as plt
from sklearn.linear_model import LinearRegression

st.write("""
# Stock Price Analysis with charts

The data displayed is from **Microsoft** showing changes in opening, closing, low, high, and volume prices in a decade between 2014 and 2024
""")

#define the ticker symbol for Microsoft
tickerSymbol = 'MSFT'
#get data on this ticker from yfinance library
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker in this century
tickerDf = tickerData.history(period='1mo', start='2014-5-31', end='2024-2-26')

# Calculate daily returns
tickerDf['Returns'] = tickerDf['Close'].pct_change()

st.write("""
## Opening Prices
""")
open_chart = st.line_chart(tickerDf['Open'])

st.write("""
## Closing Prices
""")
close_chart = st.line_chart(tickerDf['Close'])

st.write("""
## High Prices
""")
high_chart = st.line_chart(tickerDf['High'])

st.write("""
## Low Prices
""")
low_chart = st.line_chart(tickerDf['Low'])

st.write("""
## Volume Prices
""")
volume_chart = st.bar_chart(tickerDf['Volume'])

st.write("""
    To show a better relationship between the opening, closing, high, and low prices, the following candlestick graph is plotted
""")
fig = plt.Figure(data=[plt.Candlestick(x=tickerDf.index,
                                       open=tickerDf['Open'],
                                       high=tickerDf['High'],
                                       low=tickerDf['Low'],
                                       close=tickerDf['Close'])])
# Customization of the chart
fig.update_layout(
    title='Candlestick Chart',
    xaxis_title='Date',
    yaxis_title='Price'
)

st.plotly_chart(fig)

# Analyze the data in this data frame
# Calculate correlation between opening and closing prices
correlation_A = tickerDf['Open'].corr(tickerDf['Close'])
correlation_B = tickerDf['High'].corr(tickerDf['Low'])
correlation_C = tickerDf['Volume'].corr(tickerDf['High'])

# Display correlation coefficient
st.write("""
### Correlation Analysis
""")
st.write(f"The correlation coefficient between Opening and Closing prices is: {correlation_A}")
st.write(f"The correlation coefficient between High and Low prices is: {correlation_B}")
st.write(f"The correlation coefficient between Volume and High prices is: {correlation_C}")

# Volatility Analysis
st.write("""
## Volatility Analysis
""")
st.write("### Daily Returns")
st.line_chart(tickerDf['Returns'])

# Calculate and display volatility metrics
volatility_std = tickerDf['Returns'].std()
volatility_atr = tickerDf['High'].sub(tickerDf['Low']).mean()

st.write(f"Standard Deviation of Returns (Volatility): {volatility_std}")
st.write(f"Average True Range (ATR): {volatility_atr}")

# Trend Analysis
st.write("""
## Trend Analysis
""")
# Prepare the data for linear regression
X = np.arange(len(tickerDf)).reshape(-1, 1)
y = tickerDf['Close'].values.reshape(-1, 1)

# Fit linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict closing prices using the linear regression model
y_pred = model.predict(X)

# Plot the closing prices with the trend line
fig_trend = plt.Figure()
fig_trend.add_trace(plt.Scatter(x=tickerDf.index, y=tickerDf['Close'], mode='lines', name='Closing Prices'))
fig_trend.add_trace(plt.Scatter(x=tickerDf.index, y=y_pred.flatten(), mode='lines', name='Trend Line'))
fig_trend.update_layout(title='Closing Prices with Trend Line', xaxis_title='Date', yaxis_title='Closing Price')
st.plotly_chart(fig_trend)