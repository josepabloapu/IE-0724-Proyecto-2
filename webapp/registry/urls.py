from django.urls import path, include
#from django.contrib.auth import login
from . import views
from .views import registro_usuario

urlpatterns = [
    path('', views.home, name="home"),
    path('assets/list', views.assets_list, name='asset_list'),
    path('assets/read/<int:pk>', views.assets_read, name='asset_read'),
    path('assets/delete/<int:pk>', views.assets_delete, name='asset_delete'),
    #path('', login, {'template_name': 'index.html'}, name='login'),
    #path('', views.login_manager, name='login_manager'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro', registro_usuario, name='registro_usuario'),
    path('new/', views.new, name='new')
]
