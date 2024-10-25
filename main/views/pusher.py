from rest_framework.decorators import api_view, permission_classes
import json
from rest_framework.response import Response
from ..models import Account
from ..signals import pusher_client
@api_view(['POST'])
def pusher_authentication(request):
    user = Account.objects.get(email=request.user)

    auth = pusher_client.authenticate(
        channel=request.form['channel_name'],
        socket_id=request.form['socket_id'],
        custom_data={
        u'user_id': user.id,
        }
    )
    return Response(json.dumps(auth))