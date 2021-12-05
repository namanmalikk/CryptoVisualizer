from django.shortcuts import render
import pandas as pd


def home(request):
    return render(request, "home.html")


def cryptoDetail(request, pk):
    coin_name = pk
    url = f"C:\\Users\\naman\\Desktop\\DS-Project\\DSDashboard\\Datasets\\{coin_name}.csv"
    df = pd.read_csv(url)

    df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

    daily_dates = []
    daily_price = []

    for dt in df['Date']:
        date = dt.strftime("%d/%m/%Y")
        year = dt.strftime("%Y")
        daily_dates.append(date)

    for op, cp in zip(df['Open'], df['Close']):
        price_mean = (op+cp)/2
        daily_price.append(round(price_mean, 4))

    # print(len(daily_dates))
    # print(len(daily_price))
    # for i in range(len(daily_dates)):
    #     print(daily_dates[i],daily_price[i])

    peak_price = 0
    peak_price_date = None

    for dh, dt in zip(df['High'], df['Date']):
        if dh > peak_price:
            peak_price = max(peak_price, dh)
            date = dt.strftime("%d/%m/%Y")
            peak_price_date = dt

    min_price = float('inf')
    min_price_date = None

    for dl, dt in zip(df['Low'], df['Date']):
        if dl < min_price:
            min_price = min(min_price, dl)
            date = dt.strftime("%d/%m/%Y")
            min_price_date = date

    # print(min_price,min_price_date)

    # print(peak_price,peak_price_date)

    # print(df.head())

    context = {
        'coin_name': coin_name,
        'daily_dates': daily_dates,
        'daily_price': daily_price,
        'peak_price': peak_price,
        'peak_price_date': peak_price_date,
        'min_price': min_price,
        'min_price_date': min_price_date,
    }

    return render(request, "detail.html", context)
