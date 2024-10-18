from django.urls import path, re_path, include
from . views import account, team

urlpatterns = [
    path('accounts/', account.account_list),
    path('accounts/<int:pk>/', account.account_detail),
    path('accounts/me/', account.my_account),
    path('teams/', team.team_list),
    path('teams/<int:pk>/', team.team_detail),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]