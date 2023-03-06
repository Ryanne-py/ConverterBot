import requests
from bs4 import BeautifulSoup
import lxml
from art import tprint


class CurrencyNameError(Exception):
    pass


def conversion(start_currency: str,
               quantity_currency: str,
               end_currency: str) -> float:
    """
    input:(str(start_currency), int(quantity), str(end_currency))
    output:final quantity
        """

    try:
        start_currency = start_currency.lower()
        end_currency = end_currency.lower()

        if quantity_currency.isdigit() is False:
            raise AttributeError

        url = f'https://minfin.com.ua/ua/currency/converter/' \
              f'{quantity_currency}-{start_currency}-to-{end_currency}/' \
              f'?converter-type=auction'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        result = soup.find_all('input', class_='sc-11fozao-1 kWXTOP')

        return result[1].get('value')

    except AttributeError:
        raise TypeError('Wrong data types in passed arguments')

    except IndexError:
        raise CurrencyNameError('Wrong currency code')


def main():
    tprint('currency converter')
    start_currency = input('start_currency[code: str]:')
    end_currency = input('end_currency[code: str]:')
    quantity_currency = input('quantity_currency[count: int]')
    print(conversion(start_currency, quantity_currency, end_currency))


if __name__ == '__main__':
    main()