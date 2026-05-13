from io import BytesIO

from django.http import FileResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import ContactMessage
from .pdf import build_resume_pdf


def download_resume(request):
    resume_html = render_to_string('resume.html', request=request)
    pdf_file = BytesIO(build_resume_pdf(resume_html))

    return FileResponse(
        pdf_file,
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
