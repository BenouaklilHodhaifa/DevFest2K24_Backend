from django.urls import path, re_path, include

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls.jwt')),
]