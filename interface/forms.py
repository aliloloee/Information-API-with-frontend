from django import forms



class DoctorConsiderationForm(forms.Form) :
    considerations = forms.CharField(label='Considerations', help_text='Required',
                                    widget=forms.Textarea(attrs={'rows': 15}))

    def clean_considerations(self) :
        considerations = self.cleaned_data['considerations']
        if considerations == '' :
            return forms.ValidationError('Consideration can not be empty')
        return considerations

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['considerations'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Considerations'})