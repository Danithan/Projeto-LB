from django.urls import path
from . import views

app_name = 'sessoes'

urlpatterns = [
    path('iniciar/<int:crianca_id>/', views.escolher_sessao, name='escolher_sessao'),
    path('<int:sessao_id>/', views.sessao_detail, name='sessao_detail'),
]
