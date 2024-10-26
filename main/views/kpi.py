from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .. import serializers
from rest_framework.response import Response
from ..models import KPI, Account, Notification, InterestGroups
from ..signals import real_time_update
from datetime import timedelta
from main.signals import real_time_update
import re
from main.ai_models.classify.pure import predict as classify_kpi
from main.ai_models.forecast.prediction import forecast


def to_snake_case(text):
    # First, convert CamelCase or PascalCase to snake_case
    text = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
    # Convert spaces and hyphens to underscores
    text = re.sub(r'[\s\-]+', '_', text)
    # Remove any duplicate underscores
    text = re.sub(r'_+', '_', text)
    return text

@api_view(['POST'])
@permission_classes([AllowAny])
def log_kpi(request):
    serializer = serializers.KPISerializer(data=request.data)
    
    if serializer.is_valid():
        kpi = serializer.save()
        model_input = []
        latest_kpi = KPI.objects.filter(kpi_name=kpi.kpi_name).latest('timestamp')
        base_time = latest_kpi.timestamp
        time_frame = [base_time - timedelta(minutes=50), base_time]
        kpis = KPI.objects.filter(kpi_name=kpi.kpi_name, timestamp__range=time_frame)
        data_serializer = serializers.KPISerializer(kpis, many=True) 
        data = []
        for d in data_serializer.data:
            data.append({'Timestamp': d['timestamp'], 'KPI_Value': d['kpi_value']})
        data.append(
            {'Timestamp': kpi.timestamp, 'KPI_Value': kpi.kpi_value}
        )
        status = False #####
        # status = classify_kpi(data=data, kpi=kpi.kpi_name)
        kpi.status = status
        kpi.save()
        # predicted future steps (with alert raising if anomaly classified)

        data = {
            "timestamp": [],
            "kpi_value": []
        }
        for d in data_serializer.data:
            data["timestamp"].append(d["timestamp"])
            data["kpi_value"].append(d["kpi_value"])
        data["timestamp"].append(kpi.timestamp)
        data["kpi_value"].append(kpi.kpi_value)

        # df = forecast(kpi.kpi_name, 10, data)
        # df["KPI_Name"] = kpi.kpi_name
        # df['Status'] = False

        predicted = [{'id': 0, 'timestamp': '2024-10-26 10:00:00', 'kpi_value': 10.5, 'status': False}, {'id': 1, 'timestamp': '2024-10-26 10:01:00', 'kpi_value': 10.6, 'status': False}, {'id': 2, 'timestamp': '2024-10-26 10:02:00', 'kpi_value': 10.8, 'status': False}, {'id': 3, 'timestamp': '2024-10-26 10:03:00', 'kpi_value': 10.7, 'status': False}, {'id': 4, 'timestamp': '2024-10-26 10:04:00', 'kpi_value': 10.9, 'status': False}, {'id': 5, 'timestamp': '2024-10-26 10:05:00', 'kpi_value': 10.2, 'status': False}, {'id': 6, 'timestamp': '2024-10-26 10:06:00', 'kpi_value': 10.4, 'status': False}, {'id': 7, 'timestamp': '2024-10-26 10:07:00', 'kpi_value': 10.6, 'status': False}, {'id': 8, 'timestamp': '2024-10-26 10:08:00', 'kpi_value': 10.3, 'status': False}, {'id': 9, 'timestamp': '2024-10-26 10:09:00', 'kpi_value': 10.5, 'status': False}, {'id': 10, 'timestamp': '2024-10-26 10:10:00', 'kpi_value': 10.7, 'status': False}, {'id': 11, 'timestamp': '2024-10-26 10:11:00', 'kpi_value': 10.6, 'status': False}, {'id': 12, 'timestamp': '2024-10-26 10:12:00', 'kpi_value': 10.8, 'status': False}, {'id': 13, 'timestamp': '2024-10-26 10:13:00', 'kpi_value': 10.9, 'status': False}, {'id': 14, 'timestamp': '2024-10-26 10:14:00', 'kpi_value': 10.2, 'status': False}, {'id': 15, 'timestamp': '2024-10-26 10:15:00', 'kpi_value': 10.3, 'status': False}, {'id': 16, 'timestamp': '2024-10-26 10:16:00', 'kpi_value': 10.5, 'status': False}, {'id': 17, 'timestamp': '2024-10-26 10:17:00', 'kpi_value': 10.8, 'status': False}, {'id': 18, 'timestamp': '2024-10-26 10:18:00', 'kpi_value': 10.4, 'status': False}, {'id': 19, 'timestamp': '2024-10-26 10:19:00', 'kpi_value': 10.3, 'status': False}, {'id': 20, 'timestamp': '2024-10-26 10:20:00', 'kpi_value': 10.7, 'status': False}, {'id': 21, 'timestamp': '2024-10-26 10:21:00', 'kpi_value': 10.2, 'status': False}, {'id': 22, 'timestamp': '2024-10-26 10:22:00', 'kpi_value': 10.6, 'status': False}, {'id': 23, 'timestamp': '2024-10-26 10:23:00', 'kpi_value': 10.5, 'status': False}, {'id': 24, 'timestamp': '2024-10-26 10:24:00', 'kpi_value': 10.8, 'status': False}, {'id': 25, 'timestamp': '2024-10-26 10:25:00', 'kpi_value': 10.4, 'status': False}, {'id': 26, 'timestamp': '2024-10-26 10:26:00', 'kpi_value': 10.9, 'status': False}, {'id': 27, 'timestamp': '2024-10-26 10:27:00', 'kpi_value': 10.6, 'status': False}, {'id': 28, 'timestamp': '2024-10-26 10:28:00', 'kpi_value': 10.3, 'status': False}, {'id': 29, 'timestamp': '2024-10-26 10:29:00', 'kpi_value': 10.5, 'status': False}, {'id': 30, 'timestamp': '2024-10-26 10:30:00', 'kpi_value': 10.7, 'status': False}, {'id': 31, 'timestamp': '2024-10-26 10:31:00', 'kpi_value': 10.9, 'status': False}, {'id': 32, 'timestamp': '2024-10-26 10:32:00', 'kpi_value': 10.6, 'status': False}, {'id': 33, 'timestamp': '2024-10-26 10:33:00', 'kpi_value': 10.4, 'status': False}, {'id': 34, 'timestamp': '2024-10-26 10:34:00', 'kpi_value': 10.8, 'status': False}, {'id': 35, 'timestamp': '2024-10-26 10:35:00', 'kpi_value': 10.3, 'status': False}, {'id': 36, 'timestamp': '2024-10-26 10:36:00', 'kpi_value': 10.5, 'status': False}, {'id': 37, 'timestamp': '2024-10-26 10:37:00', 'kpi_value': 10.2, 'status': False}, {'id': 38, 'timestamp': '2024-10-26 10:38:00', 'kpi_value': 10.7, 'status': False}, {'id': 39, 'timestamp': '2024-10-26 10:39:00', 'kpi_value': 10.9, 'status': False}, {'id': 40, 'timestamp': '2024-10-26 10:40:00', 'kpi_value': 10.8, 'status': False}, {'id': 41, 'timestamp': '2024-10-26 10:41:00', 'kpi_value': 10.4, 'status': False}, {'id': 42, 'timestamp': '2024-10-26 10:42:00', 'kpi_value': 10.6, 'status': False}, {'id': 43, 'timestamp': '2024-10-26 10:43:00', 'kpi_value': 10.5, 'status': False}, {'id': 44, 'timestamp': '2024-10-26 10:44:00', 'kpi_value': 10.2, 'status': False}, {'id': 45, 'timestamp': '2024-10-26 10:45:00', 'kpi_value': 10.7, 'status': False}, {'id': 46, 'timestamp': '2024-10-26 10:46:00', 'kpi_value': 10.3, 'status': False}, {'id': 47, 'timestamp': '2024-10-26 10:47:00', 'kpi_value': 10.4, 'status': False}, {'id': 48, 'timestamp': '2024-10-26 10:48:00', 'kpi_value': 10.8, 'status': False}, {'id': 49, 'timestamp': '2024-10-26 10:49:00', 'kpi_value': 10.9, 'status': False}]

        # for i in range(1, 11):
        #     predicted.append({
        #         'timestamp': df.index[-i],
        #         'kpi_value': df['KPI_Value'][-i],
        #         'status': df['Status'][-i]
        #     })

        real_time_update.send(
        sender=None,
        channel=to_snake_case(kpi.kpi_name),
        event='new_data',
        data={
            "history": serializer.data,
            "predicted": predicted
        }
        )
        if kpi.status == True:
            Notification.objects.create(
                title = "Out Of Norm",
                content = f"KPI {kpi.kpi_name} is out of norm",
                interest_group = InterestGroups.MANAGERS_INTEREST_GROUP
            )	
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def kpi_list(request):
    user = Account.objects.get(email=request.user)
    kpi_name = request.query_params.get('kpi_name', None)
    if not kpi_name:
        return Response({'error': 'kpi_name request param wasn\'t set'}, status=400)
    try:
        latest_kpi = KPI.objects.filter(kpi_name=kpi_name).latest('timestamp')
    except KPI.DoesNotExist:
        return Response({'error': 'No KPIs found for the given name'}, status=404)

    base_time = latest_kpi.timestamp
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

