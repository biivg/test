import yfinance          as yf
import ta                as ta
import matplotlib.pyplot as plt
import streamlit         as st

df      = yf.download("BTC-USD", start = "2023-01-01")
close   = df['Close']

len     = st.number_input('rsi len:', min_value = 1, value = 15)  
len_ema = st.number_input('ema len:', min_value = 1, value = 31)  

# Calculate RSI
rsi = ta.momentum.RSIIndicator(close, len).rsi()

# Calculate EMA of RSI
ema = ta.trend.EMAIndicator(rsi, len_ema).ema_indicator()

# Conditions for long and short
L = ema > 50
S = ema < 50

# Plotting
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

# Plotting the closing price of BTC-USD
axes[0].plot(df.index, close, label='BTC-USD Close Price', color = 'black')
axes[0].set_yscale('log')  # Set the y-axis to a logarithmic scale
axes[0].set_title('BTC-USD Close Price and RSI EMA Indicator')
axes[0].legend()

# Highlighting the areas where conditions are met
axes[0].fill_between(df.index, close, where = L, color='green', alpha=0.3)
axes[0].fill_between(df.index, close, where = S, color='red', alpha=0.3)

# Plotting RSI and its EMA on the second subplot
axes[1].plot(df.index, rsi, label='RSI', color='#490082')
axes[1].plot(df.index, ema, label='EMA of RSI', color='orange', linestyle='-')
axes[1].hlines(50, df.index[0], df.index[-1], colors='gray', linestyles='--')  # 50 level for reference (mid-line rsi)

axes[1].set_title('RSI and EMA of RSI')
axes[1].legend()

# Showing the plot on Streamlit
st.pyplot(fig)
