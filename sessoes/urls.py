from django.urls import path
from . import views

app_name = 'sessoes'

urlpatterns = [
    path('<int:sessao_id>/', views.sessao_detail, name='sessao_detail'),
]
