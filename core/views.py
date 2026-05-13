from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render

from .models import ContactMessage


def download_resume(request):
    file_path = settings.RESUME_PDF_PATH

    if not file_path.exists():
        raise Http404("Resume file not found.")

    return FileResponse(
        file_path.open('rb'),
        as_attachment=True,
        filename='Yali_Tal_Resume.pdf',
        content_type='application/pdf',
    )


def resume_view(request):
    if request.method == "POST":
        # Get data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database
        ContactMessage.objects.create(
            name=name, email=email, subject=subject, message=message
        )
        return render(request, 'resume.html', {'success': True})

    return render(request, 'resume.html')
