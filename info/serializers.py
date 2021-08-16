from django.conf import settings
from django.db.models import fields

from rest_framework import serializers

from customUser.models import User, DefinedPeople
from .models import Information, ECGInformation
from .serializers_utils import ChoiceField, DateField, TimeStampField
from persian_tools import national_id
from datetime import datetime


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class InformationSerializer(DynamicFieldsModelSerializer):

    gender = ChoiceField(choices=Information.GENDER)
    blood_type = ChoiceField(choices=Information.BLOOD)
    marital_status = ChoiceField(choices=Information.MARITAL_STATUS)

    congenital_disease = ChoiceField(choices=Information.REGULAR)
    diabetes_disease_background = ChoiceField(choices=Information.REGULAR)
    hereditary_disease_background = ChoiceField(choices=Information.REGULAR)
    surgery = ChoiceField(choices=Information.REGULAR)
    alcohol_consumption_background = ChoiceField(choices=Information.REGULAR)
    tobacco_consumption_background = ChoiceField(choices=Information.REGULAR)
    medical_allergy_background = ChoiceField(choices=Information.REGULAR)
    food_allergy_background = ChoiceField(choices=Information.REGULAR)
    emotional_shock_background = ChoiceField(choices=Information.REGULAR)
    single_child = ChoiceField(choices=Information.REGULAR)
    nearby_waves = ChoiceField(choices=Information.REGULAR)

    menopausal_condition = ChoiceField(choices=Information.FEMALE_ONLY_REGULAR)
    irregular_menopausal = ChoiceField(choices=Information.FEMALE_ONLY_REGULAR)
    birth_giving = ChoiceField(choices=Information.CHILDBIRTH)

    surgery_date = DateField(
        input_formats=['%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', ])

    def request_ispatch(self):
        if self.context['request_method'] == 'PATCH':
            return True
        return False

    class Meta:
        model = Information
        fields = '__all__'
        read_only_fields = ("created", "updated", "slug",
                            "doctor_considerations", )

    def validate_national_id(self, value):
        if national_id.validate(value):
            return value
        raise serializers.ValidationError('Wrong national id')

    def validate_weight(self, value):
        if value < 0 or value > 999:
            raise serializers.ValidationError('Wrong wight')
        return round(value, 1)

    def validate_height(self, value):
        if value < 0 or value > 999:
            raise serializers.ValidationError('Wrong height')
        return round(value, 1)

    def validate_male_childern_numbe(self, value):
        if type(value) != int or value < 0 or value > 99:
            raise serializers.ValidationError(
                'Wrong input for number of male children')
        return value

    def validate_female_childern_number(self, value):
        if type(value) != int or value < 0 or value > 99:
            raise serializers.ValidationError(
                'Wrong input for number of female children')
        return value

    def validate(self, attrs):
        if self.request_ispatch():
            return self.validate_patch(attrs)

        # Congenital Disease
        if attrs['congenital_disease'] == 'no' and attrs['congenital_disease_description'] != '':
            raise serializers.ValidationError(
                "Congenital disease can't have description")

        # Hereditary Disease Background
        if attrs['hereditary_disease_background'] == 'no' and attrs['hereditary_disease_description'] != '':
            raise serializers.ValidationError(
                "Hereditary disease can't have description")

        # Surgery
        if attrs['surgery'] == 'no' and attrs['surgery_description'] != '':
            raise serializers.ValidationError("Surgery can't have description")
        if attrs['surgery'] == 'no' and attrs['surgery_date'] != None:
            raise serializers.ValidationError(
                "Surgery can't have description or date")

        # Alcohol
        if attrs['alcohol_consumption_background'] == 'no' and attrs['alcohol_consumption_description'] != '':
            raise serializers.ValidationError(
                "Alcohol consumption disease can't have description")

        # Tobacco
        if attrs['tobacco_consumption_background'] == 'no' and attrs['tobacco_consumption_description'] != '':
            raise serializers.ValidationError("Tobacco can't have description")
        if attrs['tobacco_consumption_background'] == 'no' and attrs['tobacco_type'] != '':
            raise serializers.ValidationError("Tobacco can't have any type")

        # Medical allergy
        if attrs['medical_allergy_background'] == 'no' and attrs['medical_allergy_description'] != '':
            raise serializers.ValidationError(
                "Medical allergy can't have description")

        # Food allergy
        if attrs['food_allergy_background'] == 'no' and attrs['food_allergy_description'] != '':
            raise serializers.ValidationError(
                "Food allergy can't have description")

        # Emotional shock
        if attrs['emotional_shock_background'] == 'no' and attrs['emotional_shock_description'] != '':
            raise serializers.ValidationError(
                "Emotional shock can't have description")

        # Child number
        if attrs['single_child'] == 'yes' and attrs['child_number'] != '':
            raise serializers.ValidationError("Child number is not needed")

        # Nearby waves
        if attrs['nearby_waves'] == 'no' and attrs['nearby_waves_description'] != '':
            raise serializers.ValidationError(
                "Nearby waves can't have description")

        # Female-only fields
        if attrs['gender'] == 'male':
            if attrs['menopausal_condition'] != '' or attrs['irregular_menopausal'] != '' or attrs['birth_giving'] != '':
                raise serializers.ValidationError(
                    "Only females fill these fields : menopausal_condition, irregular_menopausal and birth_giving")
        if attrs['gender'] == 'female':
            if attrs['menopausal_condition'] == '---------' or attrs['irregular_menopausal'] == '---------' or attrs['birth_giving'] == '---------':
                raise serializers.ValidationError(
                    "Females must fill these fields : menopausal_condition, irregular_menopausal and birth_giving")

        return attrs

    # Only when request method is PATCH
    def validate_patch(self, attrs):
        # Congenital Disease
        try:
            atr = attrs['congenital_disease']
        except:
            pass
        else:
            try:
                if atr == 'no' and attrs['congenital_disease_description'] != '':
                    raise ValueError(
                        "Congenital disease can't have description")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of congenital_disease")

        # Hereditary Disease Background
        try:
            atr = attrs['hereditary_disease_background']
        except:
            pass
        else:
            try:
                if atr == 'no' and attrs['hereditary_disease_description'] != '':
                    raise ValueError(
                        "Hereditary disease can't have description")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of hereditary_disease_background")

        # Surgery
        try:
            atr = attrs['surgery']
        except:
            pass
        else:
            try:
                if atr == 'no' and attrs['surgery_description'] != '':
                    raise ValueError("Surgery can't have description")
                if atr == 'no' and attrs['surgery_date'] != None:
                    raise ValueError("Surgery can't have description or date")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of surgery")

        # Alcohol
        try:
            atr = attrs['alcohol_consumption_background']
        except:
            pass
        else:
            try:
                if atr == 'no' and attrs['alcohol_consumption_description'] != '':
                    raise ValueError(
                        "Alcohol consumption disease can't have description")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of alcohol_consumption_background")

        # Tobacco
        try:
            atr = attrs['tobacco_consumption_background']
        except:
            pass
        else:
            try:
                if atr == 'no' and attrs['tobacco_consumption_description'] != '':
                    raise ValueError("Tobacco can't have description")
                if atr == 'no' and attrs['tobacco_type'] != '':
                    raise ValueError("Tobacco can't have any type")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of tobacco_consumption_background")

        # Medical allergy
        try:
            atr = attrs['medical_allergy_background']
        except:
            pass
        else:
            try:
                if atr == 'no' and attrs['medical_allergy_description'] != '':
                    raise ValueError("Medical allergy can't have description")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of medical_allergy_background")

        # Food allergy
        try:
            atr = attrs['food_allergy_background']
        except:
            pass
        else:
            try:
                if atr == 'no' and attrs['food_allergy_description'] != '':
                    raise ValueError("Food allergy can't have description")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of food_allergy_background")

        # Emotional shock
        try:
            atr = attrs['emotional_shock_background']
        except:
            pass
        else:
            try:
                if atr == 'no' and attrs['emotional_shock_description'] != '':
                    raise ValueError("Emotional shock can't have description")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of emotional_shock_background")

        # Child number
        try:
            atr = attrs['single_child']
        except:
            pass
        else:
            try:
                if atr == 'yes' and attrs['child_number'] != '':
                    raise ValueError("Child number is not needed")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of single_child")

        # Nearby waves
        try:
            atr = attrs['nearby_waves']
        except:
            pass
        else:
            try:
                if attrs['nearby_waves'] == 'no' and attrs['nearby_waves_description'] != '':
                    raise ValueError("Nearby waves can't have description")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of nearby_waves")

        # Female-only fields
        try:
            atr = attrs['gender']
        except:
            pass
        else:
            try:
                if attrs['gender'] == 'male':
                    if attrs['menopausal_condition'] != '' or attrs['irregular_menopausal'] != '' or attrs['birth_giving'] != '':
                        raise ValueError(
                            "Only females fill these fields : menopausal_condition, irregular_menopausal and birth_giving")
                if attrs['gender'] == 'female':
                    if attrs['menopausal_condition'] == '---------' or attrs['irregular_menopausal'] == '---------' or attrs['birth_giving'] == '---------':
                        raise ValueError(
                            "Females must fill these fields : menopausal_condition, irregular_menopausal and birth_giving")
            except ValueError as e:
                raise serializers.ValidationError(e)
            except:
                raise serializers.ValidationError(
                    "Provide dependent field(s) of gender")

        return attrs

    def create(self, validated_data):
        obj = super().create(validated_data)
        obj.save()
        return obj


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'fullname', 'password', )

    def validate_username(self, value):
        if not national_id.validate(value):
            raise serializers.ValidationError('Wrong username')
        exists = User.objects.filter(username=value)
        if exists:
            raise serializers.ValidationError('Username already exists')
        return value

    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                'Password can not be less than 5 characters')
        return value

    def set_user_type(self, validated_data):
        try:
            defined_user = DefinedPeople.objects.get(
                national_id=validated_data['username'])
        except:
            defined_user = None

        if defined_user == None:
            return User.USER_TYPE_CHOICES[-1]

        if defined_user.user_type == 1:
            return DefinedPeople.TYPE_CHOICES[0]
        elif defined_user.user_type == 2:
            return DefinedPeople.TYPE_CHOICES[1]
        elif defined_user.user_type == 3:
            return DefinedPeople.TYPE_CHOICES[2]

    def create(self, validated_data):
        user = super().create(validated_data)

        user_type, role = self.set_user_type(validated_data)
        if role in ('doctor', 'nurse', 'patient', ):
            user.user_type = user_type
        else:
            if role == 'staff':
                user.is_staff = True

        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'fullname', )

# * As it was said in the models, creating a model with manytomany field is different(read from models). Also here when
# * serializer.save() gets called, the model instance gets created just like the process explained in the models.


class ECGInformationSerializer(serializers.ModelSerializer):
    recorded_at = TimeStampField()
    nurse = NurseSerializer(read_only=True)

    class Meta:
        model = ECGInformation
        fields = '__all__'
        read_only_fields = ("nurse", "created", "updated", "slug", )

    def validate_ecg(self, value):
        file_type = value.content_type

        if file_type not in settings.ECG_SUPPORTED_FILE_FORMAT:
            raise serializers.ValidationError('File not supported')

        if value.size > settings.MAX_ECG_FILE_SIZE:
            raise serializers.ValidationError('File is too big')
        return value

    def create(self, validated_data):
        validated_data['nurse'] = self.context['nurse']
        ecginfo = super().create(validated_data)
        # ecginfo.nurse = self.context['nurse']
        # ecginfo.save()
        return ecginfo


class DoctorUsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'fullname', 'username', )
