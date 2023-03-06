import requests
import json


class PrivatAPI:

    def __init__(self):
        pass

    def get_cash_rate(self):
        response: requests.Response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
        response = json.loads(response.text)
        currency_info = []
        for i in response:
            currency_info.append(f"{i['base_ccy']} -> {i['ccy']}\nBuy - {i['buy']} Sale - {i['sale']}\n")
        return ''.join(currency_info)

    def get_сashless_rate(self):
        response: requests.Response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11')
        response = json.loads(response.text)
        currency_info = []
        for i in response:
            currency_info.append(f"{i['base_ccy']} -> {i['ccy']}\nBuy - {i['buy']} Sale - {i['sale']}\n")
        return ''.join(currency_info)