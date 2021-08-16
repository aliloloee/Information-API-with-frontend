from django.contrib import admin
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import models

from .models import Information, ECGInformation, DoctorConsideration


@admin.register(DoctorConsideration)
class DoctorConsiderationAdmin(admin.ModelAdmin) :
    list_display = ('get_doctor_name', 'ecg', )

    @admin.display(description='Doctor')
    def get_doctor_name(self, obj) :
        return f'{obj.doctor.fullname}'

@admin.register(Information)
class InformationAdmin(admin.ModelAdmin) :
    model = Information
    list_display = ('national_id', 'fullname', 'pk')
    readonly_fields = ('slug', )


@admin.register(ECGInformation)
class ECGInformationAdmin(admin.ModelAdmin) :
    list_display = ('get_patient_national_id', 'get_patient_name', )
    search_fields = ('patient__fullname', 'patient__national_id', 'doctor__fullname', )
    readonly_fields = ('recorded_at', 'slug', )
    # * searching for : patient name, doctor name, patient national id, 

    @admin.display(description='NATIONAL ID')
    def get_patient_national_id(self, obj) :
        return f'{obj.patient.national_id}'

    @admin.display(description='FULLNAME')
    def get_patient_name(self, obj) :
        return f'{obj.patient.fullname}'

    # After changing the ecg file we need to delete the previouse file
    def save_model(self, request, obj, form, change):
        if change :
            if form.initial['ecg'] != form.cleaned_data['ecg'] :
                media_url = settings.MEDIA_URL
                try :
                    ecg = ECGInformation.objects.get(pk=obj.pk).ecg.url
                    path = ecg.strip(media_url)
                    default_storage.delete(path)
                except :
                    pass

        return super().save_model(request, obj, form, change)