from customUser.models import User
from rest_framework import permissions


## Staff Users
class IsStaff(permissions.BasePermission) :
    def has_permission(self, request, view) :
        try :
            User.objects.get(username=request.query_params['username'])
        except :
            return False

        if request.user.is_staff :
            return True

## Superuser
class IsSuper(permissions.BasePermission) :
    def has_permission(self, request, view) :
        try :
            User.objects.get(user_name=request.query_params['username'])
        except :
            return False

        if request.user.is_superuser :
            return True

## Owner
class IsOwner(permissions.BasePermission) :
    def has_permission(self, request, view) :
        try :
            user = User.objects.get(user_name=request.query_params['username'])
        except :
            return False

        if not user == request.user :
            return False
        else :
            return True

## Doctor users
class IsDoctor(permissions.BasePermission) :
    def has_permission(self, request, view) :

        try :
            user_type = request.user.user_type
        except :
            return False

        if user_type == User.USER_TYPE_CHOICES[0][0] :
            return True
        else :
            return False

## Nurse users
class IsNurse(permissions.BasePermission) :
    def has_permission(self, request, view) :

        try :
            user_type = request.user.user_type
        except :
            return False

        if user_type == User.USER_TYPE_CHOICES[1][0] :
            return True
        else :
            return False

## Patient users
class IsPatient(permissions.BasePermission) :
    def has_permission(self, request, view) :

        try :
            user_type = request.user.user_type
        except :
            return False

        if user_type == User.USER_TYPE_CHOICES[2][0] :
            return True
        else :
            return False
