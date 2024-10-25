from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .. import serializers
from rest_framework.response import Response
from ..models import KPI, Account
from ..signals import real_time_update
from datetime import datetime, timedelta
from django.utils import timezone
from main.signals import real_time_update
import inflection
import re

def to_snake_case(text):
    # Convert CamelCase or PascalCase to snake_case
    text = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
    # Convert spaces and hyphens to underscores
    text = re.sub(r'[\s\-]+', '_', text)
    return text

@api_view(['POST'])
@permission_classes([AllowAny])
def log_kpi(request):
    serializer = serializers.KPISerializer(data=request.data)
    
    if serializer.is_valid():
        kpi = serializer.save()

        real_time_update.send(
        sender=None,
        channel=to_snake_case(kpi.kpi_name),
        event='new_data',
        data=serializer.data
        )

        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def kpi_list(request):
    user = Account.objects.get(email=request.user)
    kpi_name = request.query_params.get('kpi_name', None)
    if not kpi_name:
        return Response({'error': 'kpi_name request param wasn\'t set'}, status=400)
    
    base_time = datetime.strptime("2017-05-21 17:15:00+00:00", "%Y-%m-%d %H:%M:%S%z")
    time_frame = [base_time - timedelta(hours=1), base_time]
    if user.has_perm('main.view_kpi'):
        kpis = KPI.objects.filter(kpi_name=kpi_name, timestamp__range=time_frame)
        serializer = serializers.KPISerializer(kpis, many=True)
        response = {
            'history': serializer.data,
            'predicted': []
        }
        return Response(response)
    return Response({'error': 'You do not have permission to view KPIs'}, status=403)