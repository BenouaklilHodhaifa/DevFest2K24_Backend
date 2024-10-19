from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view


@api_view(['GET'])
def notification_list(request):
    user = Account.objects.get(email=request.user)
    interest_groups = request.query_params.getlist('interest_group', None)

    if not interest_groups:
        if user.user_type == Account.Manager:
            notifications = Notification.objects.all()
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        return Response( {'error': 'interest_group request param wasn\'t set'}, status=status.HTTP_400_BAD_REQUEST)

    if not set(interest_groups).issubset(set(InterestGroups.INTEREST_GROUPS)):
        return Response( {'error': 'interest_groups request param is invalid'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_interest_groups = user.get_interest_groups()

    if not set(interest_groups).issubset(set(user_interest_groups)):
        return Response( {'error': 'You don\'t have permission to view this interest_group'}, status=status.HTTP_403_FORBIDDEN)

    notifications = Notification.objects.filter(interest_group__in=interest_groups)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)