from django.http import JsonResponse
from currency.models import Cotacao
import requests
import datetime
from workadays import workdays as wd
from django.shortcuts import render

def index(request):

    return render(request, 'currency/index.html')


def save_api(request):
    date_now = datetime.datetime.now().date()
    data = []
    link = 'https://api.vatcomply.com/rates?'

    if request.method == "POST":
        try:
            for i in range(0, 7):
                dias = date_now - datetime.timedelta(days=i)
                if wd.is_workday(dias, country='BR'):
                    req = requests.get(link, params={"date": dias, "base": "USD"})
                    data.append(req.json())
        except Exception as e:
            print(e)

        if data:
            for i in range(len(data)):
                if Cotacao.objects.filter(data__contains=data[i]["date"]):
                    print("Cotação do dia já adiocionada. Não possui valores novos a serem inseridos")
                else:
                    p = Cotacao(
                        data = data[i]["date"],
                        dolar = data[i]["rates"]["USD"],
                        euro = data[i]["rates"]["EUR"],
                        yene = data[i]["rates"]["JPY"],
                        real = data[i]["rates"]["BRL"],
                    )

                    p.save()
                    data_atual = data[i]["date"]
                    print(f"Foi realizado atualização das cotações até o dia {data_atual}")
    
    return render(request, 'currency/index.html')

        


def cotacao(request):
    mydata = Cotacao.objects.all().values().order_by('-data')[:5]

    dic_cotacao = {
        "data": [i["data"] for i in mydata[::-1]],
        "dolar": [float(i["dolar"]) for i in mydata[::-1]],
        "euro": [float(i["euro"]) for i in mydata[::-1]],
        "yene": [float(i["yene"]) for i in mydata[::-1]],
        "real": [float(i["real"]) for i in mydata[::-1]],
    }

    highchart = {
                        'chart': {
                            'type': 'column'
                        },
                        'title': {
                            'text': 'Cotação'
                        },
                        'subtitle': {
                            'text': 'Source: api.vatcomply.com'
                        },
                        'xAxis': {
                            'type': "datetime",
                            'categories': dic_cotacao['data'],
                            'crosshair': 'true'
                        },
                        'yAxis': {
                            'min': 0,
                            'title': {
                            'text': 'Comparação de Cotação'
                            }
                        },
                        'tooltip': {
                            'headerFormat': '<span style="font-size:10px">{point.key}</span><table>',
                            'pointFormat': '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                            '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                            'footerFormat': '</table>',
                            'shared': 'true',
                            'useHTML': 'true'
                        },
                        'plotOptions': {
                            'column': {
                            'pointPadding': 0.2,
                            'borderWidth': 0
                            }
                        },
                        'series': [{
                            'name': 'dolar',
                            'data': dic_cotacao['dolar']

                        }, {
                            'name': 'euro',
                            'data': dic_cotacao['euro']

                        }, {
                            'name': 'yene',
                            'data': dic_cotacao['yene']

                        }, {
                            'name': 'real',
                            'data': dic_cotacao['real']

                        }]
                }

    return JsonResponse(highchart, safe=False)