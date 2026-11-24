from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.CategoriaListCreateView.as_view(), name='categoria_list_create'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria_detail'),
    path('productos/', views.ProductoListCreateView.as_view(), name='producto_list_create'),
    path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('auth/productos/', views.ProductoProtegidoListCreateView.as_view(), name='producto_auth_list_create'),
    path('auth/productos/<int:pk>/', views.ProductoProtegidoDetailView.as_view(), name='producto_auth_detail'),
    path('auth/status/', views.AuthCheckView.as_view(), name='auth_status'),
]
