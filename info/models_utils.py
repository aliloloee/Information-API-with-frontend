from django.db import models
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError

from persian_tools import national_id


def validate_national_id(value) :
    if not national_id.validate(value) :
        raise ValidationError('Wrong national id !!')


def file_directory_path(instance, filename):
    file_type = filename.split('.')[1]
    record_time = timezone.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f'ECG-Files/{instance.patient.national_id}/{record_time}.{file_type}'


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, max_value=None, *args, **kwargs):
        self.max_value = max_value
        models.IntegerField.__init__(self, verbose_name, *args, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class ContentTypeRestrictedFileField(FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", ['application/txt', ])
        self.max_upload_size = kwargs.pop("max_upload_size", 2621440)

        return super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):      
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass        
            
        return data