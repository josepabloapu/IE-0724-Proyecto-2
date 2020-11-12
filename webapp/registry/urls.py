from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('appointments/new', views.appointment_new, name='appointment_new'),
    path('appointments/list', views.appointment_list, name='appointment_list'),
    path('appointments/read/<int:pk>', views.appointment_read, name='appointment_read'),
    path('appointments/edit/<int:pk>', views.appointment_edit, name='appointment_edit'),
    path('appointments/delete/<int:pk>', views.appointment_delete, name='appointment_delete'),
]
