from django.shortcuts import render, redirect
from .forms import FileUploadForm

def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'outside/file_upload.html', {'form': form})

def file_upload_success(request):
    return render(request, 'outside/file_upload_success.html')
