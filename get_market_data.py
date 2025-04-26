# -*- coding: utf-8 -*-
"""Enhanced Market Report with BOE Rate and Professional Formatting"""

import yfinance as yf
import pandas as pd
import yagmail 
from datetime import datetime
import pytz
import time
import os
import requests
from bs4 import BeautifulSoup
import re
import numpy as np 
import numpy_financial as npf




tickers = {
    "Nikkei 225": "^N225",
    "Hang Seng": "^HSI",
    "SSE Composite": "000001.SS",
    "FTSE 100": "^FTSE",
    "DAX Index": "^GDAXI",
    "S&P 500 (prior day)": "^GSPC",
    "Dow Jones (prior day)": "^DJI",
    "Nasdaq Composite (prior day)": "^IXIC",
    "USD/JPY (Yen)": "JPY=X",
    "EUR/USD (Euro)": "EURUSD=X",
    "GBP/USD (Pound)": "GBPUSD=X",
    "Crude Oil (WTI)": "WTI",  
    "S&P Futures": "ES=F",
    "Dow Jones Futures": "YM=F", 
    "Nasdaq Futures": "NQ=F", 
    "Gold Futures": "GC=F",
    "US-10 Year Bond Futures": "ZN=F"  # Will be handled separately for yield conversion
}

def calculate_bond_yield(futures_price, coupon_rate=0.06, years=10, face_value=100):
    """
    Calculate approximate yield from Treasury futures price using bond math.
    Args:
        futures_price: Current ZN=F futures price
        coupon_rate: Annual coupon rate (6% is standard for 10Y Treasuries)
        years: Time to maturity
        face_value: Principal amount
    Returns:
        Implied yield in percentage
    """
    cash_flows = np.full(years, coupon_rate * face_value)
    cash_flows[-1] += face_value  # Add principal at maturity
    return npf.irr([-futures_price] + list(cash_flows)) * 100

def get_trading_economics_yields():
    yields = {}
    urls = {
        "UK 10Y Gilt Yield": "https://tradingeconomics.com/united-kingdom/government-bond-yield",
        "Germany 10Y Bond Yield": "https://tradingeconomics.com/germany/government-bond-yield",
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    for name, url in urls.items():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            match = re.search(rf"{name.split()[0]} 10Y\s+([\d.]+)", text)
            if match:
                yields[name] = f"{match.group(1)}%"
            else:
                yields[name] = "Not found"
        except Exception as e:
            yields[name] = f"Error: {str(e)}"
    return yields

def get_market_data(): 
    """Fetch market data with enhanced error handling and bond yield conversion"""
    data = []
    
    # Get standard market data
    for name, symbol in tickers.items():
        try:
            asset = yf.Ticker(symbol)
            info = asset.history(period="2d")
            
            if not info.empty and len(info) >= 2:
                last_close = info["Close"].iloc[-1]
                prev_close = info["Close"].iloc[-2]
                change = last_close - prev_close
                percent_change = (change / prev_close) * 100
                
                # Special handling for bond futures
                if name == "US-10 Year Bond Futures":
                    yield_value = calculate_bond_yield(last_close)
                    data.append([name, f"{last_close:.2f}", f"{change:.2f}", f"{percent_change:.2f}%"])
                    data.append(["US-10Y Implied Futures Yield", f"{yield_value:.2f}%", f"{change:.2f}", f"{percent_change:.2f}%"])
                else:
                    # Format numbers based on asset type      
                    if any(x in name for x in ["Nikkei", "Hang Seng", "FTSE", "DAX", "S&P", "Dow", "Nasdaq", "Gold"]):
                        data.append([name, f"{last_close:,.2f}", f"{change:,.2f}", f"{percent_change:.2f}%"])
                    elif any(x in name for x in ["USD/JPY", "EUR/USD", "GBP/USD"]):
                        data.append([name, f"{last_close:.4f}", f"{change:.4f}", f"{percent_change:.2f}%"])
                    else:  # Commodities
                        data.append([name, f"{last_close:.2f}", f"{change:.2f}", f"{percent_change:.2f}%"])
            else:
                data.append([name, "No Data", "N/A", "N/A"])

        except Exception as e:
            print(f"Error fetching {name}: {str(e)}")
            data.append([name, "Error", "Error", "Error"])

    # Append bond yields from Trading Economics
    bond_yields = get_trading_economics_yields()
    for name, value in bond_yields.items():
        data.append([name, value, "N/A", "N/A"])
    
    return pd.DataFrame(data, columns=["Asset", "Last Price", "Change", "Change %"])


if __name__ == "__main__":
    get_market_data()



