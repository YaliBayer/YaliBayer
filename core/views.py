from django.shortcuts import render, redirect
from .models import ContactMessage

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