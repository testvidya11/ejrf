import os
from django.core.exceptions import ValidationError
from django.forms import forms
from eJRF.settings import ACCEPTED_EXTENSIONS


class SupportDocumentUploadForm(forms.Form):
    file = forms.FileField(label='Support document', required=True)

    def clean_file(self):
        _file = self.cleaned_data['file']
        name, extension = os.path.splitext(str(_file))
        if extension.lower() not in ACCEPTED_EXTENSIONS:
            raise ValidationError('%s file type is not an allowed, Please upload %s files only' % (extension, ', '.join(ACCEPTED_EXTENSIONS)))
        return _file