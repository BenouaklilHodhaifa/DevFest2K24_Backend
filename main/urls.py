from django.urls import path, re_path, include
from . views import account, team
from .views import sensors_loading

urlpatterns = [
    path('accounts/', account.account_list),
    path('accounts/<int:pk>/', account.account_detail),
    path('accounts/me/', account.my_account),
    path('teams/', team.team_list),
    path('teams/<int:pk>/', team.team_detail),
    re_path(r'^auth/', include('djoser.urls.jwt')),
	path('sensors-loading/welding', sensors_loading.welding),
	path('sensors-loading/stamping-press', sensors_loading.stamping_press),
	path('sensors-loading/painting-robot', sensors_loading.painting_robot),
	path('sensors-loading/agv', sensors_loading.agv),
	path('sensors-loading/cnc-milling', sensors_loading.cnc_milling),
	path('sensors-loading/leak-test', sensors_loading.leak_test),


]