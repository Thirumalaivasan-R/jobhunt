from django.urls import path
from .views import home, job_detail

urlpatterns = [
    path('',home,name = 'home'),
    path('<int:job_id>/', job_detail, name='job_detail'),
]
