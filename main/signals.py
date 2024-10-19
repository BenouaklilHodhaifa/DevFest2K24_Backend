from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from pusher_push_notifications import PushNotifications
import environ
import os
from pathlib import Path

# # a signal to be sent when a user account is created, we didn't use the built-in django signal because
# # we are using transaction.atomic() and the post_save signal will be sent after .save() is called and not after a successfull transaction
# user_account_saved = Signal()

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:

        beams_client = PushNotifications(
            instance_id=env('PUSHER_INSTANCE_ID'),
            secret_key=env('PUSHER_PRIMARY_KEY'),
        )

        response = beams_client.publish_to_interests(
        interests=[instance.interest_group],
        publish_body={
            'web': {
            'notification': {
                'title': instance.title,
                'body': instance.content,
                'deep_link': 'localhost:3000',
            },
            },
        },
        )

        print(response)