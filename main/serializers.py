from rest_framework import serializers
from .models import *
from django.db import transaction

from django.contrib.auth import get_user_model 
User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    profile = serializers.JSONField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'user_type', 'profile']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'user_type': {'required': False}
            }

    def create(self, validated_data):      
        profile_data = validated_data.pop('profile')
        user_type = validated_data.pop('user_type', None)
        if not user_type:
            raise serializers.ValidationError("user_type field is required.")

        validated_data['username'] = validated_data['email']

        with transaction.atomic():
            user = User.objects.create_user(user_type=user_type, **validated_data)

            if user_type == User.Manager:
                user.is_staff = True
                user.is_superuser = True
                user.save()

            profile_data = self.context['request'].data.get('profile', {})

            match user_type:
                case User.Manager:
                    self.create_manager_profile(user, profile_data)
                
                case User.Operator:
                    self.create_operator_profile(user, profile_data)
                
                case _:
                    raise ValueError("Invalid user type")
        
        # user_account_saved.send(sender=self.__class__, user=user, user_type=user_type, created=True)
        return user
    
    def update(self, instance, validated_data):
        instance.personal_phone_number = validated_data.get('personal_phone_number', instance.personal_phone_number)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)    
        instance.save()
                
        return instance
    
    def create_manager_profile(self, user, profile_data):
        ManagerProfile.objects.create(user=user, **profile_data)
    
    def create_operator_profile(self, user, profile_data):
        teams_ids = profile_data.pop('teams', None)
        teams = []
        for team_id in teams_ids:
            try:
                team = Team.objects.get(pk=team_id)
                teams.append(team)
            except Team.DoesNotExist:
                raise serializers.ValidationError(f'Team with id {team_id} does not exist')

        OperatorProfile.objects.create(user=user, **profile_data)
        
        for team in teams:
            team.operators.add(user)
            team.save()

class AccountSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'profile']

    def get_profile(self, obj):
        if obj.user_type == User.Manager:
            return ManagerProfileSerializer(obj.manager_profile).data
        elif obj.user_type == User.Operator:
            return OperatorProfileSerializer(obj.operator_profile).data
        return None

class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = ['id', 'user']

class TeamSerializer(serializers.ModelSerializer):
    operators = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), many=True, required=False)
    class Meta:
        model = Team
        fields = ['id', 'name', 'machine_id', 'operators', 'interest_group']
        extra_kwargs = {
            'operators': {'required': False}
        }
    
    def create(self, validated_data):
        operators_data = validated_data.pop('operators', [])
        team = super().create(validated_data)
        team.operators.set(operators_data)
        team.save()
        return team
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['operators'] = AccountSerializer(instance.operators.all(), many=True).data
        return response

class OperatorProfileSerializer(serializers.ModelSerializer):
    teams = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='user.teams')
    class Meta:
        model = OperatorProfile
        fields = ['id', 'teams']

class WeldingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Welding
		fields = "__all__"

class StampingPressSerializer(serializers.ModelSerializer):
	class Meta:
		model = StampingPress
		fields = "__all__" 

class PaintingRobotSerializer(serializers.ModelSerializer):
	class Meta:
		model = PaintingRobot
		fields = "__all__"

class AGVSerializer(serializers.ModelSerializer):
	class Meta:
		model = AGV
		fields = "__all__"

class CNCMillingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CNCMilling
		fields = "__all__"

class LeakTestSerializer(serializers.ModelSerializer):
	class Meta:
		model = LeakTest
		fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'content', 'interest_group', 'timestamp']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'content', 'interest_group', 'timestamp', 'status', 'completed_timestamp']

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'