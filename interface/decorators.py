from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from info.models import ECGInformation, Information


def is_doctor(function):
    def wrap(request, *args, **kwargs):

        if request.user.user_type == 1 :
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def info_permission(function):
    def wrap(request, *args, **kwargs):

        information = get_object_or_404(Information, pk=kwargs['pk'], slug=kwargs['slug'])
        if information.ecg.filter(doctors__in=[request.user.pk, ]).exists() :
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def ecg_permission(function):
    def wrap(request, *args, **kwargs):

        ecg = get_object_or_404(ECGInformation, pk=kwargs['pk'], slug=kwargs['slug'])
        if request.user in ecg.doctors.all() :
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap