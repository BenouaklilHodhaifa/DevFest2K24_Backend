from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .. import serializers
from django.http import JsonResponse
from ..models import Notification
from random import random


norms = {
	
	"welding" : {
		"weld_temperature" : {"type" : "QUANT", "vals" : (10, 1000)},
		"weld_current" : {"type" : "QUANT", "vals" : (10, 1000)},
		"weld_voltage" : {"type" : "QUANT", "vals" : (10, 1000)},
		"weld_time" : {"type" : "QUANT", "vals" : (10, 1000)},
		"pressure_applied" : {"type" : "QUANT", "vals" : (10, 1000)},
		"arm_position_x" : {"type" : "QUANT", "vals" : (10, 1000)},
		"arm_position_y" : {"type" : "QUANT", "vals" : (10, 1000)},
		"arm_position_z" : {"type" : "QUANT", "vals" : (10, 1000)},
		"wire_feed_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
		"gas_flow_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
		"weld_strength_estimate" : {"type" : "QUANT", "vals" : (10, 1000)},
		"vibration_level" : {"type" : "QUANT", "vals" : (10, 1000)},
		"power_consumption" : {"type" : "QUANT", "vals" : (10, 1000)},
		"production_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
	},

	"stamping_press" : {
		"force_applied": {"type" : "QUANT", "vals" : (10, 1000)},
		"cycle_time": {"type" : "QUANT", "vals" : (10, 1000)},
		"temperature": {"type" : "QUANT", "vals" : (10, 1000)},
		"vibration_level": {"type" : "QUANT", "vals" : (10, 1000)},
		"cycle_count": {"type" : "QUANT", "vals" : (10, 1000)},
		"oil_pressure": {"type" : "QUANT", "vals" : (10, 1000)},
		"die_alignment": {"type" : "QUAL", "vals" : ("aligned",)},
		"sheet_thickness": {"type" : "QUANT", "vals" : (10, 1000)},
		"power_consumption": {"type" : "QUANT", "vals" : (10, 1000)},
		"noise_level": {"type" : "QUANT", "vals" : (10, 1000)},
		"lubrication_flow_rate": {"type" : "QUANT", "vals" : (10, 1000)},
		"production_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
	},

	"painting_robot" : {
		"spray_pressure" : {"type" : "QUANT", "vals" : (10, 1000)},
		"paint_thickness" : {"type" : "QUANT", "vals" : (10, 1000)},
		"arm_position_x" : {"type" : "QUANT", "vals" : (10, 1000)},
		"arm_position_y" : {"type" : "QUANT", "vals" : (10, 1000)},
		"arm_position_z" : {"type" : "QUANT", "vals" : (10, 1000)},
		"temperature" : {"type" : "QUANT", "vals" : (10, 1000)},
		"humidity" : {"type" : "QUANT", "vals" : (10, 1000)},
		"paint_flow_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
		"paint_volume_used" : {"type" : "QUANT", "vals" : (10, 1000)},
		"atomizer_speed" : {"type" : "QUANT", "vals" : (10, 1000)},
		"overspray_capture_efficiency" : {"type" : "QUANT", "vals" : (10, 1000)},
		"booth_airflow_velocity" : {"type" : "QUANT", "vals" : (10, 1000)},
		"solvent_concentration" : {"type" : "QUANT", "vals" : (10, 1000)},
		"power_consumption" : {"type" : "QUANT", "vals" : (10, 1000)},
		"production_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
	},

	"agv" : {
		"location_x": {"type" : "QUANT", "vals" : (10,1000)},
		"location_y": {"type" : "QUANT", "vals" : (10,1000)},
		"location_z": {"type" : "QUANT", "vals" : (10,1000)},
		"battery_level": {"type" : "QUANT", "vals" : (10,1000)},
		"load_weight": {"type" : "QUANT", "vals" : (10,1000)},
		"speed": {"type" : "QUANT", "vals" : (10,1000)},
		"distance_traveled": {"type" : "QUANT", "vals" : (10,1000)},
		"obstacle_detection": {"type" : "QUAL", "vals" : ("yes",)},
		"navigation_status": {"type" : "QUAL", "vals" : ("en_route",)},
		"vibration_level": {"type" : "QUANT", "vals" : (10,1000)},
		"temperature": {"type" : "QUANT", "vals" : (10,1000)},
		"wheel_rotation_speed": {"type" : "QUANT", "vals" : (10,1000)},
		"power_consumption" : {"type" : "QUANT", "vals" : (10, 1000)},
		"production_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
	},

	"cnc_milling" : {
		"spindle_speed" : {"type" : "QUANT", "vals" : (10, 1000)},
		"tool_wear_level" : {"type" : "QUANT", "vals" : (10, 1000)},
		"cut_depth" : {"type" : "QUANT", "vals" : (10, 1000)},
		"feed_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
		"vibration_level" : {"type" : "QUANT", "vals" : (10, 1000)},
		"coolant_flow_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
		"material_hardness" : {"type" : "QUANT", "vals" : (10, 1000)},
		"power_consumption" : {"type" : "QUANT", "vals" : (10, 1000)},
		"temperature" : {"type" : "QUANT", "vals" : (10, 1000)},
		"chip_load" : {"type" : "QUANT", "vals" : (10, 1000)},
		"production_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
	},

	"leak_test" : {
		"test_pressure" : {"type" : "QUANT", "vals" : (10, 1000)},
		"pressure_drop" : {"type" : "QUANT", "vals" : (10, 1000)},
		"leak_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
		"test_duration" : {"type" : "QUANT", "vals" : (10, 1000)},
		"temperature" : {"type" : "QUANT", "vals" : (10, 1000)},
		"status" : {"type" : "QUAL", "vals" : ("pass",)},
		"seal_condition" : {"type" : "QUAL", "vals" : ("good",)},
		"test_cycle_count" : {"type" : "QUANT", "vals" : (10, 1000)},
		"power_consumption" : {"type" : "QUANT", "vals" : (10, 1000)},
		"production_rate" : {"type" : "QUANT", "vals" : (10, 1000)},
	},
}

def fill_OON(data, norm):
	defect = False
	new_data = dict(data)
	for key, val in norms[norm].items():
		OON_state = not (val["vals"][0] < data[key] < val["vals"][1] if val["type"] == "QUANT" else data[key] in val["vals"])
		defect = defect or OON_state
		new_data[key+"_OON"] = OON_state
	return new_data, defect

@api_view(['POST'])
@permission_classes([AllowAny])
def welding(request):
	processed_data = dict(request.data)
	# Adding a random production_rate for simulation
	processed_data["production_rate"] = 20 * random()
	processed_data["arm_position_x"] = request.data["arm_position"]["x"]
	processed_data["arm_position_y"] = request.data["arm_position"]["y"]
	processed_data["arm_position_z"] = request.data["arm_position"]["z"]
	processed_data.pop("arm_position")
	processed_data, defect = fill_OON(processed_data, "welding")
	if defect :
		Notification.objects.create(
			title = "Welding Machine Defect",
			content = "Some fields retured by the sensor were Out Of Norm",
			interest_group = Notification.WELDING_INTEREST_GROUP
		)
	serializer = serializers.WeldingSerializer(data = processed_data)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def stamping_press(request):
	processed_data = dict(request.data)
	# Adding a random production_rate for simulation
	processed_data["production_rate"] = 20 * random()
	processed_data, defect = fill_OON(request.data, "stamping_press")
	if defect :
		Notification.objects.create(
			title = "Stamping Machine Defect",
			content = "Some fields retured by the sensor were Out Of Norm",
			interest_group = Notification.STAMPING_PRESS_INTEREST_GROUP
		)	
	serializer = serializers.StampingPressSerializer(data = processed_data)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def painting_robot(request):
	processed_data = dict(request.data)
	# Adding a random production_rate for simulation
	processed_data["production_rate"] = 20 * random()
	processed_data["power_consumption"] = 20 * random.random()
	processed_data["arm_position_x"] = request.data["arm_position"]["x"]
	processed_data["arm_position_y"] = request.data["arm_position"]["y"]
	processed_data["arm_position_z"] = request.data["arm_position"]["z"]
	processed_data.pop("arm_position")
	processed_data, defect = fill_OON(processed_data, "painting_robot")
	if defect :
		Notification.objects.create(
			title = "Painting Machine Defect",
			content = "Some fields retured by the sensor were Out Of Norm",
			interest_group = Notification.PAINTING_ROBOT_INTEREST_GROUP
		)
	serializer = serializers.PaintingRobotSerializer(data = processed_data)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def agv(request):
	processed_data = dict(request.data)
	# Adding a random production_rate for simulation
	processed_data["production_rate"] = 20 * random()
	# Adding a randomly generated power_consumption field for simulation
	processed_data["power_consumption"] = 20 * random()
	processed_data["location_x"] = request.data["location"]["x"]
	processed_data["location_y"] = request.data["location"]["y"]
	processed_data["location_z"] = request.data["location"]["z"]
	processed_data.pop("location")
	processed_data, defect = fill_OON(processed_data, "agv")
	if defect :
		Notification.objects.create(
			title = "AGV Machine Defect",
			content = "Some fields retured by the sensor were Out Of Norm",
			interest_group = Notification.AGV_INTEREST_GROUP
		)	
	serializer = serializers.AGVSerializer(data = processed_data)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def cnc_milling(request):
	processed_data = dict(request.data)
	# Adding a random production_rate for simulation
	processed_data["production_rate"] = 20 * random()
	processed_data, defect = fill_OON(request.data, "cnc_milling")
	if defect :
		Notification.objects.create(
			title = "CNC Machine Defect",
			content = "Some fields retured by the sensor were Out Of Norm",
			interest_group = Notification.CNC_MILLING_INTEREST_GROUP
		)
	serializer = serializers.CNCMillingSerializer(data = processed_data)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def leak_test(request):
	processed_data = dict(request.data)
	# Adding a random production_rate for simulation
	processed_data["production_rate"] = 20 * random()
	# Adding a randomly generated power_consumption data field for simulation
	processed_data["power_consumption"] = 20 * random()
	processed_data, defect = fill_OON(request.data, "leak_test")
	if defect :
		Notification.objects.create(
			title = "Leak Machine Defect",
			content = "Some fields retured by the sensor were Out Of Norm",
			interest_group = Notification.LEAK_TEST_INTEREST_GROUP
		)
	serializer = serializers.LeakTestSerializer(data = processed_data)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)