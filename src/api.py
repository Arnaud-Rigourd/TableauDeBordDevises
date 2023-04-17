from collections import defaultdict
from datetime import datetime, timedelta, date
from pprint import pprint

import requests


BASE_URL = 'https://api.exchangerate.host/'


def get_rates(currencies: str, days: int = 30) -> tuple[list[str], dict[str, list[float]]]:
    url = _get_request_elements(currencies, days)["url"]
    params = _get_request_elements(currencies, days)["params"]
    response = requests.get(url, params=params)
    if not response and not response.json():
        return False, False  # type: ignore

    data = response.json()
    api_rates = data.get("rates")
    all_days = sorted(api_rates.keys())
    all_rates = _get_rates_by_currency([api_rates[key] for key in api_rates])

    return all_days, all_rates


def _get_rates_by_currency(rates: list[dict[str, float]]) -> dict[str, list[float]]:
    rates_by_currency = defaultdict(list)
    for rate in rates:
        for key, value in rate.items():
            rates_by_currency[key].append(value)

    return dict(rates_by_currency)


def _get_request_elements(currencies: str, days: int) -> dict[str, dict]:
    get_request_elements = {}
    days_in_url = _format_days_for_url(days)
    currencies_in_url = _format_currencies_for_url(currencies)
    params = {
        "base": "EUR",
        "symbols": currencies_in_url
    }

    get_request_elements["url"] = BASE_URL + days_in_url
    get_request_elements["params"] = params

    return get_request_elements


def _format_days_for_url(days: int) -> str:
    delta = timedelta(days=days - 1)
    start_date = (datetime.today() - delta)
    end_date = datetime.today()
    date_in_url = f"timeseries?start_date={start_date}&end_date={end_date}"
    return date_in_url


def _format_currencies_for_url(currencies: str) -> str:
    asked_currencies = [i.strip().upper() for i in currencies.split(",")]
    if _check_currencies(asked_currencies):
        currencies_in_url = ",".join(asked_currencies)
        return currencies_in_url
    else:
        return "L'une des devise n'est pas répertoriée dans la DB"


def _check_currencies(asked_currencies: list[str]) -> bool:
    api_currencies = _get_api_currencies(BASE_URL + "latest")
    if all(i in api_currencies for i in asked_currencies):
        return True
    return False


def _get_api_currencies(url: str = BASE_URL) -> list:
    response = requests.get(url)
    data = response.json()
    currencies = [i for i in data["rates"]]
    return currencies


if __name__ == '__main__':
    days, rates = get_rates("usd, cad")
    pprint(days)
    pprint(rates)
