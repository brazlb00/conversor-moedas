import requests
import datetime as datetime
from workadays import workdays as wd

# date_now = datetime.datetime.now().date()
# seven_days_ago = date_now - datetime.timedelta(days=7)

# print(f'Dia {seven_days_ago}, é dia útil? ', wd.is_workday(seven_days_ago, country='BR', years=range(2020, 2023)))

# data = {}

date_now = datetime.datetime.now().date()
data = []
new_dict = []
link = 'https://api.vatcomply.com/rates?'

for i in range(0, 7):
    days = date_now - datetime.timedelta(days=i)
    if wd.is_workday(days, country='BR'):
        req = requests.get(link, params={"date": days, "base": "USD"})
        data.append(req.json())

for i in range(len(data)):
    new_dict.append(
        {
            "data": data[i]["date"], 
            "USD": data[i]["rates"]["USD"], 
            "EUR": data[i]["rates"]["EUR"], 
            "JPY": data[i]["rates"]["JPY"],
            "BRL": data[i]["rates"]["BRL"]
        },
    )

print(new_dict)


# req = requests.get(link, params={"date": "2023-04-17", "base": "USD"})
# print(req.json())