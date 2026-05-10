from django.contrib import admin
from django.urls import path
from core.views import resume_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', resume_view, name='home'),
]