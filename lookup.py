import yfinance as yf

while True:
    ticker_input = input("Enter a ticker (Type exit to quit): ").upper()
    if ticker_input.lower() == 'exit':
        break
    else:
        try:
            ticker = yf.Ticker(ticker_input)
            info = ticker.info
            print(f"{ticker_input}")
            print(f"Company Name: {info.get('longName', 'N/A')}")
            print(f"Sector: {info.get('sector', 'N/A')}")
            print(f"Market Cap: {info.get('marketCap', 'N/A')}")
            print(f"Current Price: {info.get('currentPrice', 'N/A')}")
            print("52-Week Low:", info.get("fiftyTwoWeekLow", "N/A"))
            print("52-Week High:", info.get("fiftyTwoWeekHigh", "N/A"))
    
        except Exception as e:
            print(f"Invalid ticker.")
