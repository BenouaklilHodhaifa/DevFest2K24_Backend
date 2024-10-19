from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from django.utils import timezone


@api_view(['GET'])
def task_list(request):
    user = Account.objects.get(email=request.user)
    interest_groups = request.query_params.getlist('interest_group', None)

    if not interest_groups:
        if user.user_type == Account.Manager:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        return Response( {'error': 'interest_group request param wasn\'t set'}, status=status.HTTP_400_BAD_REQUEST)

    if not set(interest_groups).issubset(set(InterestGroups.INTEREST_GROUPS)):
        return Response( {'error': 'interest_groups request param is invalid'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_interest_groups = user.get_interest_groups()

    if not set(interest_groups).issubset(set(user_interest_groups)):
        return Response( {'error': 'You don\'t have permission to view this interest_group'}, status=status.HTTP_403_FORBIDDEN)

    tasks = Task.objects.filter(interest_group__in=interest_groups)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def change_status_in_progress(request, pk):
    user = Account.objects.get(email=request.user)
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user_interest_groups = user.get_interest_groups()

    if task.interest_group not in user_interest_groups:
        return Response( {'error': 'You don\'t have permission to change the status of this task'}, status=status.HTTP_403_FORBIDDEN)

    task.status = Task.STATUS_IN_PROGRESS
    task.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['PUT'])
def change_status_done(request, pk):
    user = Account.objects.get(email=request.user)
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user_interest_groups = user.get_interest_groups()

    if task.interest_group not in user_interest_groups:
        return Response( {'error': 'You don\'t have permission to change the status of this task'}, status=status.HTTP_403_FORBIDDEN)

    task.status = Task.STATUS_DONE
    task.completed_timestamp = timezone.now()
    task.save()
    return Response(status=status.HTTP_200_OK)
