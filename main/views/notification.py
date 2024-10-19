from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view


@api_view(['GET'])
def notification_list(request):
    user = Account.objects.get(email=request.user)
    interest_group = request.query_params.get('interest_group', None)
    if interest_group not in InterestGroups.INTEREST_GROUPS:
        return Response( {'error': 'interest_group request param is invalid'}, status=status.HTTP_400_BAD_REQUEST)
    if not interest_group:
        if user.user_type == Account.Manager:
            notifications = Notification.objects.all()
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        return Response( {'error': 'interest_group request param wasn\'t set'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_interest_group = []
    if user.user_type == Account.Manager:
        user_interest_group = InterestGroups.INTEREST_GROUPS
    else:
        teams = user.operator_profile.teams.all()
        user_interest_group = [team.interest_group for team in teams]
    if interest_group not in user_interest_group:
        return Response( {'error': 'You don\'t have permission to view this interest_group'}, status=status.HTTP_403_FORBIDDEN)

    notifications = Notification.objects.filter(interest_group=interest_group)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)