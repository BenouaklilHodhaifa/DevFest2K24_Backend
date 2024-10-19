from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

class InterestGroups:
    MANAGERS_INTEREST_GROUP = 'managers'
    WELDING_INTEREST_GROUP = 'welding'
    STAMPING_PRESS_INTEREST_GROUP = 'stamping_press'
    PAINTING_ROBOT_INTEREST_GROUP = 'painting_robot'
    AGV_INTEREST_GROUP = 'agv'
    CNC_MILLING_INTEREST_GROUP = 'cnc_milling'
    LEAK_TEST_INTEREST_GROUP = 'leak_test'
    
    INTEREST_GROUPS = [MANAGERS_INTEREST_GROUP, WELDING_INTEREST_GROUP, STAMPING_PRESS_INTEREST_GROUP, 
                    PAINTING_ROBOT_INTEREST_GROUP, AGV_INTEREST_GROUP, CNC_MILLING_INTEREST_GROUP, 
                              LEAK_TEST_INTEREST_GROUP]

class UserAccountManager(BaseUserManager): 
    def create_user(self, email, password=None, user_type=None, **extra_fields): 
        if not email:
            raise ValueError('The Email field must be set')
        if not user_type:
            raise ValueError('The User Type field must be set')
        if user_type not in Account.user_types:
            raise ValueError('Invalid User Type')

        email = self.normalize_email(email)

        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', Account.Manager) 

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save()

        ManagerProfile.objects.create(user=user)
        # from .signals import user_account_saved
        # user_account_saved.send(sender=self.__class__, user=user, user_type=Account.SuperAdmin, created=True)

        return user

class Account(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)

    Manager = 1
    Operator = 2

    user_types = [Manager, Operator]

    user_type = models.PositiveSmallIntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    objects = UserAccountManager()

    # class Meta:
    #     permissions = (
    #         ('assign_secteur_to_livreur', 'Can a secteur to a livreur'),
    #         ('change_livreur_days_off', 'Can change livreur days off'),
    #     )

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=255)
    machine_id = models.CharField(max_length=255, unique=True)
    interest_group = models.CharField(max_length=255)
    operators = models.ManyToManyField(Account, related_name='teams')

class ManagerProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='manager_profile')

class OperatorProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='operator_profile')

# Machines

class Welding(models.Model):
	machine_id = models.CharField(max_length=100)
	weld_temperature = models.FloatField(help_text="Temperature in °C")
	weld_current = models.FloatField(help_text="Current in A (amperes)")
	weld_voltage = models.FloatField(help_text="Voltage in V")
	weld_time = models.FloatField(help_text="Weld time in milliseconds")
	pressure_applied = models.FloatField(help_text="Pressure in N (newtons)")
	arm_position_x = models.FloatField(help_text="X coordinate of the arm position")
	arm_position_y = models.FloatField(help_text="Y coordinate of the arm position")
	arm_position_z = models.FloatField(help_text="Z coordinate of the arm position")
	wire_feed_rate = models.FloatField(help_text="Wire feed rate in mm/min")
	gas_flow_rate = models.FloatField(help_text="Gas flow rate in l/min")
	weld_strength_estimate = models.FloatField(help_text="Estimated weld strength in N")
	vibration_level = models.FloatField(help_text="Vibration level in mm/s")
	power_consumption = models.FloatField(help_text="Power consumption in kWh")
	production_rate = models.FloatField(help_text="Production rate of the machine")
	# Out Of Norm fields
	weld_temperature_OON = models.BooleanField()
	weld_current_OON = models.BooleanField()
	weld_voltage_OON = models.BooleanField()
	weld_time_OON = models.BooleanField()
	pressure_applied_OON = models.BooleanField()
	arm_position_x_OON = models.BooleanField()
	arm_position_y_OON = models.BooleanField()
	arm_position_z_OON = models.BooleanField()
	wire_feed_rate_OON = models.BooleanField()
	gas_flow_rate_OON = models.BooleanField()
	weld_strength_estimate_OON = models.BooleanField()
	vibration_level_OON = models.BooleanField()
	power_consumption_OON = models.BooleanField()
	production_rate_OON = models.BooleanField()
	

	timestamp = models.DateTimeField(help_text="Timestamp of the data")

	def __str__(self):
		return f"Machine {self.machine_id} - {self.timestamp}"

class StampingPress(models.Model):
	machine_id = models.CharField(max_length=100)
	force_applied = models.FloatField(help_text="Force applied in tons")
	cycle_time = models.FloatField(help_text="Cycle time in seconds")
	temperature = models.FloatField(help_text="Temperature in °C")
	vibration_level = models.FloatField(help_text="Vibration level in mm/s")
	cycle_count = models.IntegerField(help_text="Count of cycles")
	oil_pressure = models.FloatField(help_text="Oil pressure in bar")
	die_alignment = models.CharField(max_length=100, help_text="Die alignment status")
	sheet_thickness = models.FloatField(help_text="Sheet thickness in mm")
	power_consumption = models.FloatField(help_text="Power consumption in kWh")
	production_rate = models.FloatField(help_text="Production rate of the machine")
	noise_level = models.FloatField(help_text="Noise level in dB")
	lubrication_flow_rate = models.FloatField(help_text="Lubrication flow rate in ml/min")

	# Out Of Norm fields
	force_applied_OON = models.BooleanField()
	cycle_time_OON = models.BooleanField()
	temperature_OON = models.BooleanField()
	vibration_level_OON = models.BooleanField()
	cycle_count_OON = models.BooleanField()
	oil_pressure_OON = models.BooleanField()
	die_alignment_OON = models.BooleanField()
	sheet_thickness_OON = models.BooleanField()
	power_consumption_OON = models.BooleanField()
	noise_level_OON = models.BooleanField()
	lubrication_flow_rate_OON = models.BooleanField()
	production_rate_OON = models.BooleanField()

	timestamp = models.DateTimeField(help_text="Timestamp of the data")

	def __str__(self):
		return f"Machine {self.machine_id} - {self.timestamp}"

class PaintingRobot(models.Model):
	machine_id = models.CharField(max_length=100)
	spray_pressure = models.FloatField(help_text="Spray pressure in bar")
	paint_thickness = models.FloatField(help_text="Paint thickness in μm (microns)")
	arm_position_x = models.FloatField(help_text="X coordinate of the arm position")
	arm_position_y = models.FloatField(help_text="Y coordinate of the arm position")
	arm_position_z = models.FloatField(help_text="Z coordinate of the arm position")
	temperature = models.FloatField(help_text="Temperature in °C")
	humidity = models.FloatField(help_text="Humidity in %RH")
	paint_flow_rate = models.FloatField(help_text="Paint flow rate in ml/min")
	paint_volume_used = models.FloatField(help_text="Paint volume used in liters")
	atomizer_speed = models.FloatField(help_text="Atomizer speed in RPM")
	overspray_capture_efficiency = models.FloatField(help_text="Overspray capture efficiency in %")
	booth_airflow_velocity = models.FloatField(help_text="Booth airflow velocity in m/s")
	solvent_concentration = models.FloatField(help_text="Solvent concentration in %")
	power_consumption = models.FloatField(help_text="Power consumption in kWh")
	production_rate = models.FloatField(help_text="Production rate of the machine")
	# Out Of Norm fields
	spray_pressure_OON = models.BooleanField()
	paint_thickness_OON = models.BooleanField()
	arm_position_x_OON = models.BooleanField()
	arm_position_y_OON = models.BooleanField()
	arm_position_z_OON = models.BooleanField()
	temperature_OON = models.BooleanField()
	humidity_OON = models.BooleanField()
	paint_flow_rate_OON = models.BooleanField()
	paint_volume_used_OON = models.BooleanField()
	atomizer_speed_OON = models.BooleanField()
	overspray_capture_efficiency_OON = models.BooleanField()
	booth_airflow_velocity_OON = models.BooleanField()
	solvent_concentration_OON = models.BooleanField()
	power_consumption_OON = models.BooleanField()
	production_rate_OON = models.BooleanField()

	timestamp = models.DateTimeField(help_text="Timestamp of the data")

	def __str__(self):
		return f"Machine {self.machine_id} - {self.timestamp}"
    
class AGV(models.Model):
	machine_id = models.CharField(max_length=100)
	location_x = models.FloatField(help_text="X coordinate of the location")
	location_y = models.FloatField(help_text="Y coordinate of the location")
	location_z = models.FloatField(help_text="Z coordinate of the location")
	battery_level = models.FloatField(help_text="Battery level in %")
	load_weight = models.FloatField(help_text="Load weight in kg")
	speed = models.FloatField(help_text="Speed in m/s")
	distance_traveled = models.FloatField(help_text="Distance traveled in meters")
	obstacle_detection = models.CharField(max_length=100, choices=[('yes', 'Yes'), ('no', 'No')], help_text="Obstacle detection status")
	navigation_status = models.CharField(max_length=100, choices=[('en_route', 'En Route'), ('waiting', 'Waiting'), ('rerouting', 'Rerouting')], help_text="Navigation status")
	vibration_level = models.FloatField(help_text="Vibration level in mm/s")
	temperature = models.FloatField(help_text="Temperature in °C")
	wheel_rotation_speed = models.FloatField(help_text="Wheel rotation speed in RPM")
	power_consumption = models.FloatField(help_text="Power consumption in kWh")
	production_rate = models.FloatField(help_text="Production rate of the machine")
	# Out Of Norm fields
	location_x_OON = models.BooleanField()
	location_y_OON = models.BooleanField()
	location_z_OON = models.BooleanField()
	battery_level_OON = models.BooleanField()
	load_weight_OON = models.BooleanField()
	speed_OON = models.BooleanField()
	distance_traveled_OON = models.BooleanField()
	obstacle_detection_OON = models.BooleanField()
	navigation_status_OON = models.BooleanField()
	vibration_level_OON = models.BooleanField()
	temperature_OON = models.BooleanField()
	wheel_rotation_speed_OON = models.BooleanField()
	power_consumption_OON = models.BooleanField()
	production_rate_OON = models.BooleanField()

	timestamp = models.DateTimeField(help_text="Timestamp of the data")

	def __str__(self):
		return f"Machine {self.machine_id} - {self.timestamp}"

class CNCMilling(models.Model):
	machine_id = models.CharField(max_length=100)
	spindle_speed = models.FloatField(help_text="Spindle speed in RPM")
	tool_wear_level = models.FloatField(help_text="Tool wear level in %")
	cut_depth = models.FloatField(help_text="Cut depth in mm")
	feed_rate = models.FloatField(help_text="Feed rate in mm/min")
	vibration_level = models.FloatField(help_text="Vibration level in mm/s")
	coolant_flow_rate = models.FloatField(help_text="Coolant flow rate in ml/min")
	material_hardness = models.FloatField(help_text="Material hardness in HB (Brinell hardness)")
	power_consumption = models.FloatField(help_text="Power consumption in kWh")
	production_rate = models.FloatField(help_text="Production rate of the machine")
	temperature = models.FloatField(help_text="Temperature in °C")
	chip_load = models.FloatField(help_text="Chip load in mm")

	# Our Of Norm fields
	spindle_speed_OON = models.BooleanField()
	tool_wear_level_OON = models.BooleanField()
	cut_depth_OON = models.BooleanField()
	feed_rate_OON = models.BooleanField()
	vibration_level_OON = models.BooleanField()
	coolant_flow_rate_OON = models.BooleanField()
	material_hardness_OON = models.BooleanField()
	power_consumption_OON = models.BooleanField()
	production_rate_OON = models.BooleanField()
	temperature_OON = models.BooleanField()
	chip_load_OON = models.BooleanField()
	
	
	timestamp = models.DateTimeField(help_text="Timestamp of the data")

	def __str__(self):
		return f"Machine {self.machine_id} - {self.timestamp}"

class LeakTest(models.Model):
	machine_id = models.CharField(max_length=100)
	test_pressure = models.FloatField(help_text="Test pressure in bar")
	pressure_drop = models.FloatField(help_text="Pressure drop in bar")
	leak_rate = models.FloatField(help_text="Leak rate in ml/min")
	test_duration = models.FloatField(help_text="Test duration in seconds")
	temperature = models.FloatField(help_text="Temperature in °C")
	status = models.CharField(max_length=100, choices=[('pass', 'Pass'), ('fail', 'Fail')], help_text="Test status")
	fluid_type = models.CharField(max_length=100, help_text="Type of fluid used for the test")
	seal_condition = models.CharField(max_length=100, choices=[('good', 'Good'), ('warning', 'Warning'), ('fail', 'Fail')], help_text="Condition of the seal")
	test_cycle_count = models.IntegerField(help_text="Number of test cycles")
	power_consumption = models.FloatField(help_text="Power consumption in kWh")
	production_rate = models.FloatField(help_text="Production rate of the machine")
	# Out Of Norm fields
	test_pressure_OON = models.BooleanField()
	pressure_drop_OON = models.BooleanField()
	leak_rate_OON = models.BooleanField()
	test_duration_OON = models.BooleanField()
	temperature_OON = models.BooleanField()
	status_OON = models.BooleanField()
	seal_condition_OON = models.BooleanField()
	test_cycle_count_OON = models.BooleanField()
	power_consumption_OON = models.BooleanField()
	production_rate_OON = models.BooleanField()
      
	timestamp = models.DateTimeField(help_text="Timestamp of the data")

	def __str__(self):
		return f"Machine {self.machine_id} - {self.timestamp}"

class Notification(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255 )
    interest_group = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)