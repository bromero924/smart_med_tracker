from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('take-dose/<int:dose_id>/', views.take_dose, name='take_dose'),
]
