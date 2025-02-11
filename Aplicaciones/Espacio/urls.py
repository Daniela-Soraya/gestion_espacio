from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.inicio, name='inicio'),
    # Espacios
    path('espacios/', views.lista_espacios, name='lista_espacios'),
    path('espacios/crear/', views.crear_espacio, name='crear_espacio'),
    path('espacios/<int:espacio_id>/editar/', views.editar_espacio, name='editar_espacio'),
    path('espacios/eliminar/<int:pk>/', views.eliminar_espacio, name='eliminar_espacio'),

    # Proyectos
    path('proyectos/', views.lista_proyectos, name='lista_proyectos'),
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/<int:proyecto_id>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('proyectos/eliminar/<int:pk>/', views.eliminar_proyecto, name='eliminar_proyecto'),

    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),

    # Evaluaciones
    path('evaluaciones/', views.lista_evaluaciones, name='lista_evaluaciones'),
    path('evaluaciones/crear/', views.crear_evaluacion, name='crear_evaluacion'),
    path('evaluaciones/editar/<int:pk>/', views.editar_evaluacion, name='editar_evaluacion'),
    path('evaluaciones/eliminar/<int:pk>/', views.eliminar_evaluacion, name='eliminar_evaluacion'),

    #Suguerencias
    path('sugerencias/crear/', views.crear_sugerencia, name='crear_sugerencia'),  # URL para crear una nueva sugerencia
    path('sugerencias/', views.lista_sugerencias, name='lista_sugerencias'),  # URL para listar todas las sugerencias

]
