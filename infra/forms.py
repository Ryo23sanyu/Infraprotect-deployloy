from django import forms
from .models import CustomUser, UploadedFile
from .models import Photo, Company

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        
class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        
# 会社別に表示

class UserCreationForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all())

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'company')

