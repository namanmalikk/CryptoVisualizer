from django.shortcuts import render, redirect
import pandas as pd
from .forms import UploadFileForm


def home(request):
    if request.method == "POST":
        coinName = request.POST.get('selectedCoin')
        return redirect('detailView', coinName)
    return render(request, "home.html")


def cryptoDetail(request, pk):
    # we will receive name of coin as primary key from url
    coin_name = pk

    # this is the dataset url of recieved coin_name
    url = f"C:\\Users\\naman\\Desktop\\DS-Project\\DSDashboard\\Datasets\\{coin_name}.csv"

    # dataset corresponding to particular coin_name is read from url and converted to dataframe
    df = pd.read_csv(url)

    # changing date format of all rows (ex- from Nov 07, 2021 to datetime format)
    df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

    # daily_dates contains date corresponding to each row entry of dataset
    # daily_price contains mean price i.e ((open price + close price) / 2) corresponding to each row entry of dataset
    # year_list contains year corresponding to each row entry of dataset
    daily_dates = []
    daily_price = []
    year_list = []

    for dt in df['Date']:
        date = dt.strftime("%Y")
        year = dt.strftime("%Y")
        daily_dates.append(date)
        year_list.append(year)

    for op, cp in zip(df['Open'], df['Close']):
        price_mean = (op+cp)/2
        daily_price.append(round(price_mean, 4))

    # year_list will contain list of all unique years in dataset in sorted order
    year_list = list(set(year_list))
    year_list.sort()

    # peak_price contain maximum price of that coin according to dataset
    # peak_price_date contain date at which peak_price was achieved
    peak_price = 0
    peak_price_date = None

    for dh, dt in zip(df['High'], df['Date']):
        if dh > peak_price:
            peak_price = max(peak_price, dh)
            date = dt.strftime("%d/%m/%Y")
            peak_price_date = date

    # min_price contain minimum price of that coin according to dataset
    # min_price_date contain date at which min_price was achieved
    min_price = float('inf')
    min_price_date = None

    for dl, dt in zip(df['Low'], df['Date']):
        if dl < min_price:
            min_price = min(min_price, dl)
            date = dt.strftime("%d/%m/%Y")
            min_price_date = date

    # yearly_prices contain total price of all entries year corresponding to each entry in year_list
    # yearly_count contain count of total entries of year corresponding to each entry in year_list
    yearly_prices = {}
    yearly_count = {}

    for y in year_list:
        yearly_prices[y] = 0
        yearly_count[y] = 0

    for p, d in zip(daily_price, df['Date']):
        year = d.strftime("%Y")
        yearly_prices[year] += p
        yearly_count[year] += 1
        yearly_prices[year] = round(yearly_prices[year], 3)

    # year_avg contain average price of coin in a year corresponding to each entry in year_list
    year_avg = []
    for y in year_list:
        avg = yearly_prices[y]/yearly_count[y]
        year_avg.append(round(avg, 3))

    context = {
        'coin_name': coin_name,
        'daily_dates': daily_dates,
        'daily_price': daily_price,
        'peak_price': peak_price,
        'peak_price_date': peak_price_date,
        'min_price': min_price,
        'min_price_date': min_price_date,
        'year_list': year_list,
        'year_avg': year_avg,
    }

    return render(request, "detail.html", context)


def generalVisualizer(request):
    context = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES['file']
            data = pd.read_csv(file1)
            col1 = int(request.POST['feature1'])-1
            col2 = int(request.POST['feature2'])-1
            row1 = int(request.POST['startRow'])-1
            row2 = int(request.POST['endRow'])

            # filtering data based on row and column recieved from user
            x_val = data.iloc[row1:row2, col1]
            y_val = data.iloc[row1:row2, col2]
            context['x_val'] = list(x_val)
            context['y_val'] = list(y_val)
            context['chartType'] = request.POST['chartType']
    else:
        form = UploadFileForm()
    context['form'] = form
    return render(request, "visualizer.html", context)
