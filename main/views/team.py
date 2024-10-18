from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from django.db import transaction, IntegrityError
from django.db import transaction

@api_view(['GET', 'POST'])
def team_list(request):
    user = Account.objects.get(email=request.user)
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            if user.has_perm('main.add_team'):
                with transaction.atomic():
                    serializer = TeamSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except IntegrityError as e:
            return Response({'error': 'error performing create Team transaction, ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, pk):
    user = Account.objects.get(email=request.user)
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if user.has_perm('main.view_team', team):
            serializer = TeamSerializer(team)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'PUT':
        if user.has_perm('main.change_team', team):
            serializer = TeamSerializer(team, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if user.has_perm('main.delete_team', team):
            team.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)