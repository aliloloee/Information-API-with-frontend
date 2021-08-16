from rest_framework import serializers
from datetime import datetime

class TimeStampField(serializers.DateTimeField) :
    def to_internal_value(self, value):
        value = datetime.fromtimestamp(int(value))
        return super().to_internal_value(value)

class DateField(serializers.DateField) :
    def to_internal_value(self, value):
        if value == '' :
            value = None
            return value
        return super().to_internal_value(value)

class ChoiceField(serializers.ChoiceField) :
    def __init__(self, choices, *args, **kwargs) :
        self._choices = choices
        self.allow_blank = False      ## if True, then value of '' is also acceptable for the field
        super(ChoiceField, self).__init__(choices, *args, **kwargs)

    # def to_representation(self, obj):
    #     if obj == '' and self.allow_blank:
    #         return obj
    #     return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)
