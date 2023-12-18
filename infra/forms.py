from django import forms
from .models import MultiUploadedFile

class MultiFileUploadForm(forms.ModelForm):
    class Meta:
        model = MultiUploadedFile
        fields = ['files']