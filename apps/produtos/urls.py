from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    # URLs para templates (frontend)
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    
    # URLs para API (backend)
    path('api/produtos/', views.produtos_api, name='produtos_api'),
    path('api/produtos/risco/', views.produtos_risco_api, name='produtos_risco_api'),
]
