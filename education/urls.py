from django.urls import path
from . import views

urlpatterns = [
    path('', views.education_view, name='education_view'),
]