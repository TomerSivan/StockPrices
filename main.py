import requests
import csv

api_key = '0LKQ98WR53B71M1P'

def fetch_daily_stock_data(stock_symbols):
    stock_data = {}

    for symbol in stock_symbols:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            stock_data[symbol] = response.json()
        else:
            print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")
    return stock_data

def fetch_usa_stock_symbols(filename):
    usa_stock_symbols = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if (row[6] == "United States"):
                symbol = row[0]
                usa_stock_symbols.append(symbol)
    return usa_stock_symbols


def calculate_percentage_change(stock_data, date):
    percentage_changes = {}

    for symbol, data in stock_data.items():
            daily_data = data['Time Series (Daily)'][date]
            opening_price = float(daily_data['1. open'])
            closing_price = float(daily_data['4. close'])
            percentage_change = ((closing_price - opening_price) / opening_price) * 100
            percentage_changes[symbol] = percentage_change

    sorted_stocks = sorted(percentage_changes.items(), key=lambda x: x[1], reverse=True)
    top_10_stocks = sorted_stocks[:10]
    return top_10_stocks

usa_stock_symbols = fetch_usa_stock_symbols("nasdaq_screener_1695806037230.csv")
# usa_stock_symbols = ['AAPL', 'MSFT', 'GOOGL'] # For checking

date = '2023-09-26'

stock_data = fetch_daily_stock_data(usa_stock_symbols)

print(stock_data)

top_10_stocks = calculate_percentage_change(stock_data, date)

for symbol, percentage_change in top_10_stocks:
    print(f"Symbol: {symbol}, Percentage Change: {percentage_change:.2f}%")