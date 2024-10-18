from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from django.db import transaction, IntegrityError
from django.db import transaction


@api_view(['GET', 'POST'])
def account_list(request):
    user = Account.objects.get(email=request.user)

    if request.method == 'GET':
        user_type = request.query_params.get('user_type', None)
        
        accounts = Account.objects.all()

        if user_type:
            accounts = accounts.filter(user_type=int(user_type))

        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            if user.has_perm('main.add_account'):
                with transaction.atomic():
                    serializer = UserCreateSerializer(data=request.data, context={'request': request})
                    if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        except IntegrityError as e:
            return Response({'error': 'error performing create Account transaction, ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            return Response({'error': e.detail}, status=e.status_code)
        except Exception as e:
            return Response({'error': 'error performing create Account transaction, ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def account_detail(request, pk):
    user = Account.objects.get(email=request.user)
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if user.has_perm('main.view_account', account):
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'PUT':
        try: 
            if user.has_perm('main.change_account', account):   
                with transaction.atomic():
                    serializer = UserCreateSerializer(account, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except IntegrityError as e:
            return Response({'error': 'error performing update Account transaction, ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': 'error performing update Account transaction, ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        if user.has_perm('main.delete_account', account):
            account.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def my_account(request):
    user = Account.objects.get(email=request.user)
    serializer = AccountSerializer(user)
    return Response(serializer.data)

 