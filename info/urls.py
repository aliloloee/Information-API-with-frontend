from django.urls import path, re_path
from .import views
from rest_framework.routers import DefaultRouter


app_name = 'info'


router = DefaultRouter()
router.register('patient/info', views.PatientInfoViewSet)
router.register('patient/ecg', views.ECGInformationViewSet)
router.register('doctors', views.DoctorUsersViewset)


urlpatterns = [
    path('post-user', views.create_user),
    path('token', views.CustomAuthToken.as_view()),
]


urlpatterns += router.urls