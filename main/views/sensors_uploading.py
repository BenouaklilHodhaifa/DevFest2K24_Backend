from rest_framework.decorators import api_view
from .. import serializers
from .. import models
from dateutil import parser
from django.utils.timezone import make_aware
from rest_framework.response import Response


@api_view(["GET"])
def get_sensors_logs(request):

	# Parsing the GET parameters
	machine_type = request.GET.get("machine_type")
	start_timestamp = parser.parse(request.GET.get("start_timestamp"))
	end_timestamp = parser.parse(request.GET.get("end_timestamp"))

	# Making sure the timestamps are timezone aware
	if start_timestamp.tzinfo is None:
		start_timestamp = make_aware(start_timestamp)
	if end_timestamp.tzinfo is None:
		end_timestamp = make_aware(end_timestamp)
	
	if machine_type == "welding":
		query_set = models.Welding.objects.filter(timestamp__gte=start_timestamp, timestamp__lte=end_timestamp)
		serializer = serializers.WeldingSerializer(query_set, many=True)
		return Response(serializer.data, status=200)
	
	elif machine_type == "stamping_press":
		query_set = models.StampingPress.objects.filter(timestamp__gte=start_timestamp, timestamp__lte=end_timestamp)
		serializer = serializers.StampingPressSerializer(query_set, many=True)
		return Response(serializer.data, status=200)
	
	elif machine_type == "paint_robot":
		query_set = models.PaintingRobot.objects.filter(timestamp__gte=start_timestamp, timestamp__lte=end_timestamp)
		serializer = serializers.PaintingRobotSerializer(query_set, many=True)
		return Response(serializer.data, status=200)
	
	elif machine_type == "agv":
		query_set = models.AGV.objects.filter(timestamp__gte=start_timestamp, timestamp__lte=end_timestamp)
		# return Response(f"{type(query_set)}")
		serializer = serializers.AGVSerializer(query_set, many=True)
		return Response(serializer.data, status=200)
	
	elif machine_type == "cnc_milling":
		query_set = models.CNCMilling.objects.filter(timestamp__gte=start_timestamp, timestamp__lte=end_timestamp)
		serializer = serializers.CNCMillingSerializer(query_set, many=True)
		return Response(serializer.data, status=200)
	
	elif machine_type == "leak_test":
		query_set = models.LeakTest.objects.filter(timestamp__gte=start_timestamp, timestamp__lte=end_timestamp)
		serializer = serializers.LeakTestSerializer(query_set, many=True)
		return Response(serializer.data, status=200)
	
