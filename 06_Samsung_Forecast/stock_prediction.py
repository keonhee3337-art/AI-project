import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def run_prediction():
    print("--- 1. FETCHING SAMSUNG STOCK DATA ---")
    # '005930.KS' is the ticker for Samsung Electronics on Yahoo Finance
    stock = yf.Ticker("005930.KS")
    df = stock.history(period="10y")
    
    # Reset index so 'Date' becomes a regular column we can use for math
    df = df.reset_index()
    
    # PREPARE DATA FOR AI
    # Machine Learning needs numbers, not dates. 
    # We convert dates to "Ordinal numbers" (e.g., Day 1, Day 2, Day 3000)
    df['Date_Ordinal'] = df['Date'].map(pd.Timestamp.toordinal)
    
    # X = Features (The Input): The Date
    # y = Label (The Target): The Closing Price
    X = df[['Date_Ordinal']]
    y = df['Close']
    
    # SPLIT DATA (Train on the past, Test on the recent past)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    print("--- 2. TRAINING THE MODEL (Linear Regression) ---")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    print("--- 3. MAKING PREDICTIONS ---")
    # Predict prices for the test set
    predictions = model.predict(X_test)
    
    # Score the model (R^2 score: 1.0 is perfect, 0.0 is useless)
    score = model.score(X_test, y_test)
    print(f"Model Accuracy (R^2 Score): {score:.4f}")
    
    # FUTURE PREDICTION (Next 365 Days)
    last_day = df['Date_Ordinal'].iloc[-1]
    future_dates = np.array([[last_day + i] for i in range(1, 366)])
    future_prices = model.predict(future_dates)
    
    print(f"Predicted Price 1 Year form now: {future_prices[-1]:.0f} KRW")

    # VISUALIZE
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Date'], df['Close'], color='gray', s=5, label='Actual Price')
    plt.plot(df['Date'], model.predict(X), color='red', linewidth=2, label='AI Trend Line')
    plt.title(f"Samsung Electronics: AI Trend Analysis (R2: {score:.2f})")
    plt.xlabel("Date")
    plt.ylabel("Stock Price (KRW)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run_prediction()