import calendar
from datetime import datetime
from zoneinfo import ZoneInfo

from django.db.models import QuerySet, Manager, F

from quotes.settings import QUOTES_HISTORY_PERIOD


class QuotesHistoryCustomQuerySet(QuerySet):

    def get_last_history(self, currency_asset_id):
        now = datetime.now(ZoneInfo('UTC'))
        utc_now = calendar.timegm(now.utctimetuple())
        period = utc_now - QUOTES_HISTORY_PERIOD
        return self.select_related('currency_asset').filter(
            currency_asset_id=currency_asset_id, time__gte=period).annotate(
            assetName=F('currency_asset__name'),
            assertId=F('currency_asset__id'),
            value=F('quote')
        ).values(
        'assetName', 'value', 'time', 'assertId')

class QuotesHistoryCustomManager(Manager.from_queryset(QuotesHistoryCustomQuerySet)):
    pass
