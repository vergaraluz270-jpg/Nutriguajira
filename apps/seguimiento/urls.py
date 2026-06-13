from django.urls import path
from . import views

urlpatterns = [
    path('<int:paciente_id>/', views.seguimiento_paciente, name='seguimiento_paciente'),
]