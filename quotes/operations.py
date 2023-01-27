import calendar
import json
import requests
from asgiref.sync import sync_to_async
from datetime import datetime
from zoneinfo import ZoneInfo

from quotes.models import QuotesHistory, CurrencyAsset
from quotes.settings import CURRENCY_ASSETS_LIST, RATES_URL


@sync_to_async()
def get_updates():
    response = requests.get(url=RATES_URL)
    if not response.status_code == 200:
        raise Exception
    data = json.loads(response.text[5:-3])
    return data


@sync_to_async()
def get_currencies_from_list(data):
    result = {}
    for currency in data['Rates']:
        symbol = currency['Symbol']
        if symbol in CURRENCY_ASSETS_LIST:
            quote = round((currency['Bid'] + currency['Ask']) / 2, 6)
            result[symbol] = quote
    return result


@sync_to_async()
def write_new_points_and_prepare_response(data):
    #TODO rewrite to minimize number of queries to DB
    result = {}
    for symbol, quote in data.items():
        now = datetime.now(ZoneInfo('UTC'))
        utc_now = calendar.timegm(now.utctimetuple())
        symbol_instance = CurrencyAsset.objects.get(name=symbol)
        # quotes_history = QuotesHistory.objects.create(
        #     currency_asset=symbol_instance, time=utc_now, quote=quote)
        quotes_history = QuotesHistory(
            currency_asset=symbol_instance, time=utc_now, quote=quote)
        quotes_history.save()
        result[quotes_history.currency_asset_id] = {
            'message':
                {'assetName': quotes_history.currency_asset.name,
                 'time': quotes_history.time,
                 'assetId': quotes_history.currency_asset_id,
                 'value': quotes_history.quote},
            'action': 'point'
        }
    return result


@sync_to_async()
def get_assets_list():
    assets = CurrencyAsset.objects.values('id', 'name')
    asserts_list = {'action': 'assets', 'message': {'assets': list(assets)}}
    return asserts_list


@sync_to_async()
def get_asset_history(asset_id):
    history = QuotesHistory.objects.get_last_history(asset_id)
    asset_history = {
        'action': 'asset_history', 'message': {'points': list(history)}}
    return asset_history


