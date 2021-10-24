from django import forms
from django.core.exceptions import ValidationError
from core.models import Contact
from helpers.validators import validate_xlsx_file_extension


class ContactFileForm(forms.ModelForm):
    xls_file = forms.FileField(required=False, validators=[validate_xlsx_file_extension])
    name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    def clean(self):
        if not self.cleaned_data.get('xls_file'):
            if "" in self.cleaned_data.values():
                raise ValidationError("Please input either (name, phone, email) or xls file field")

    class Meta:
        model = Contact
        fields = '__all__'

