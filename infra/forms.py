from django import forms
from .models import UploadedFile, MultiUploadedFile
from .models import Photo

class MultiFileUploadForm(forms.ModelForm):
    class Meta:
        model = MultiUploadedFile
        fields = ['files']
        
class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']