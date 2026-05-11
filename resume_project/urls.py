from django.contrib import admin
from django.urls import path
from core.views import resume_view
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', resume_view, name='home'),
    path('download-resume/', views.download_resume, name='download_resume'),

]