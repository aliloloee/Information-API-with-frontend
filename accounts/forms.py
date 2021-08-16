from django import forms

from customUser.models import User

from persian_tools import national_id

class UserLoginForm(forms.Form) :
    username = forms.CharField(label='Username', help_text='Required', error_messages={'invalid' : 'Invalid Username'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username(self) :
        username = self.cleaned_data['username']

        if not national_id.validate(username) :
            return forms.ValidationError('Check your credentials')

        try :
            r = User.objects.get(username=username)
        except :
            r = None
        if not r :
            raise forms.ValidationError('Wrong crendtials')
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})