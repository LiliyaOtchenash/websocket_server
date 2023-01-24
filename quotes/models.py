from django.db import models

from quotes.managers import QuotesHistoryCustomManager


class CurrencyAsset(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=6, unique=True)

    class Meta:
        db_table = 'currency_asset'

    def __str__(self):
        return f'{self.id}_{self.name}'


class QuotesHistory(models.Model):
    currency_asset = models.ForeignKey('CurrencyAsset', on_delete=models.CASCADE)
    time = models.IntegerField()
    quote = models.FloatField()

    objects = QuotesHistoryCustomManager()

    class Meta:
        db_table = 'quotes_history'
        unique_together = (('time', 'currency_asset'),)

    def __str__(self):
        return f'currency_asset_id#{self.currency_asset}_time#{self.time}_quote#{self.quote}'
