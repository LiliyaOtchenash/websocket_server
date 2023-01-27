import json

from django.contrib.admin.models import LogEntry
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_redis import get_redis_connection


@receiver(post_save, sender='quotes.QuotesHistory')
def publish_event(sender, instance, created, **kwargs):
    if not created:
        return
    event = {
        'message':
            {'assetName': instance.currency_asset.name,
             'time': instance.time,
             'assetId': instance.currency_asset_id,
             'value': instance.quote},
        'action': 'point'
        }
    connection = get_redis_connection("default")
    payload = json.dumps(event)
    connection.publish("events", payload)

