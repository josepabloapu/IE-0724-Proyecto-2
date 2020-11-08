from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('assets/list', views.assets_list, name='asset_list'),
    path('assets/read/<int:pk>', views.assets_read, name='asset_read'),
    path('assets/delete/<int:pk>', views.assets_delete, name='asset_delete'),
]
