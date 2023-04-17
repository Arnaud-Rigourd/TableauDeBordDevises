import pytest

import api


@pytest.fixture
def url():
    return 'https://api.exchangerate.host/latest'


@pytest.fixture
def asked_currencies():
    return ["USD", "EUR", "GBP"]


def test_get_rates():
    return False


def test__get_request_elements():
    return False


def test__format_days_for_url():
    return False


def test__format_currencies_for_url():
    return False


def test__check_currencies(asked_currencies):
    assert api._check_currencies(asked_currencies) is True


def test__get_api_currencies(url):
    assert len(url) > 0
