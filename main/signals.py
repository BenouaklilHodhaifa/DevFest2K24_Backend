from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import Notification, Task
import pusher
from pusher_push_notifications import PushNotifications
import environ
import os
from pathlib import Path

real_time_update = Signal()

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

app_id = str(env('PUSHER_APP_ID'))
key = str(env('PUSHER_KEY'))
secret = str(env('PUSHER_SECRET'))
cluster = str(env('PUSHER_CLUSTER'))
pusher_client = pusher.Pusher(app_id=app_id, key=key, secret=secret, cluster=cluster)

beams_client = PushNotifications(
            instance_id=env('PUSHER_INSTANCE_ID'),
            secret_key=env('PUSHER_PRIMARY_KEY'),
        )

def send_notification(instance):   
    beams_client.publish_to_interests(
        interests=[instance.interest_group],
        publish_body={
            'web': {
            'notification': {
                'title': instance.title,
                'body': instance.content,
                'deep_link': 'http://localhost:3000',
            },
            },
        },
        )

@receiver(real_time_update)
def send_real_time_updates(channel, event, data, **kwargs):
    # channel_info = pusher_client.channel_info(channel, [u"user_count"])
    # if channel_info[u'occupied']:
    #     print("Channel is occupied")
    pusher_client.trigger(str(channel), str(event), data)
    
@receiver(post_save, sender=Notification)
def notification_created_handler(sender, instance, created, **kwargs):
    if created:
        send_notification(instance)


@receiver(post_save, sender=Task)
def task_created_handler(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            title=f"Task {instance.title} has been created",
            content=f"Task content: {instance.content}",
            interest_group=instance.interest_group
        )