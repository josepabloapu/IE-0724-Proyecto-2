from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('assets/new', views.assets_new, name='asset_new'),
    path('assets/list', views.assets_list, name='asset_list'),
    path('assets/read/<int:pk>', views.assets_read, name='asset_read'),
    path('assets/edit/<int:pk>', views.assets_edit, name='asset_edit'),
    path('assets/delete/<int:pk>', views.assets_delete, name='asset_delete'),
]
