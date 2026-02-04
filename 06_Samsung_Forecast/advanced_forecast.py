import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def run_prophet_engine():
    print("--- 1. FETCHING DATA (Samsung Electronics) ---")
    stock = yf.Ticker("005930.KS")
    df = stock.history(period="5y") # Last 5 years
    df = df.reset_index()

    # PREPARE DATA FOR PROPHET
    # Prophet demands two specific column names: 'ds' (Date) and 'y' (Value)
    data = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    
    # Remove timezones to avoid errors
    data['ds'] = data['ds'].dt.tz_localize(None)

    print("--- 2. TRAINING PROPHET MODEL ---")
    # We turn on 'daily_seasonality' because stocks trade daily
    model = Prophet(daily_seasonality=True)
    model.fit(data)

    print("--- 3. PREDICTING THE FUTURE (Next 365 Days) ---")
    # Create a list of future dates (1 year out)
    future = model.make_future_dataframe(periods=365)
    
    # The AI predicts the price for all those dates
    forecast = model.predict(future)

    # VISUALIZE
    print("--- 4. VISUALIZING ---")
    fig1 = model.plot(forecast)
    plt.title("Samsung Stock Price Forecast (1 Year Prediction)")
    plt.xlabel("Date")
    plt.ylabel("Price (KRW)")
    
    # Add a red line for today so we see where history ends and AI begins
    plt.axvline(x=data['ds'].iloc[-1], color='red', linestyle='--', label='Today')
    plt.legend()
    plt.show()

    # PRINT THE NUMBERS
    prediction_2026 = forecast.iloc[-1]
    print(f"\n🔮 AI PREDICTION for {prediction_2026['ds'].date()}:")
    print(f"   Likely Price: {prediction_2026['yhat']:.0f} KRW")
    print(f"   Best Case:    {prediction_2026['yhat_upper']:.0f} KRW")
    print(f"   Worst Case:   {prediction_2026['yhat_lower']:.0f} KRW")

if __name__ == "__main__":
    run_prophet_engine()