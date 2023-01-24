from django.conf import settings


QUOTES_HISTORY_PERIOD = getattr(
    settings, 'QUOTES_HISTORY_PERIOD', 60 * 30)  # 30 minutes in seconds

CURRENCY_ASSETS_LIST = getattr(
    settings, 'CURRENCY_ASSETS_LIST',
    ['EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD', 'USDCAD'])

RATES_URL = getattr(
    settings, 'RATES_URL', 'https://ratesjson.fxcm.com/DataDisplayer')
