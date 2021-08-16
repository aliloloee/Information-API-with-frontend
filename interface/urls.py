from django.urls import path

from . import views

app_name = 'interface'

urlpatterns = [
    path('', views.home, name='home'),
    path('history/considerd_ones/', views.ecgs_considered, name='considerd_ecgs'),
    path('info/<int:pk>/<slug:slug>/', views.patient_info, name='patient_info'),
    path('ecg/<int:pk>/<slug:slug>/', views.patient_ecg, name='patient_ecg'),
    path('nurse/<int:pk>/', views.nurse_history, name='nurse_history'),
    path('patient/<int:pk>/', views.patient_history, name='patient_history'),
    path('considerations/<int:pk>/', views.write_consideration, name='set_considerations'),
    path('update_consideration/<int:pk>/', views.update_consideration, name='update_consideration'),
]