from django.urls import path
from store_project_app import views

urlpatterns = [

    path('estadisticas', views.estadisticas, name = 'Estadisticas'),

    path('categoria', views.CategoriaListView.as_view(), name = 'Categoria'),
    path('agregar_categoria', views.CategoriaCreateView.as_view(), name = 'AgregarCategoria'),
    path('editar_categoria/<int:pk>/', views.CategoriaUpdateView.as_view(), name = 'EditarCategoria'),
    path('eliminar_categoria/<int:pk>/', views.CategoriaDeleteView.as_view(), name = 'EliminarCategoria'),
    
    path('productos', views.ProductosListView.as_view(), name = 'Productos'),

]