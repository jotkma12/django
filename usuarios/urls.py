from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),

    path('registro/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('direccion/<int:usuario_id>/', views.direccion_lista, name='direccion_lista'),
    path('direccion/<int:usuario_id>/crear/', views.direccion_crear, name='direccion_crear'),
    path('direccion/<int:usuario_id>/editar-direccion/<int:pk>/', views.direccion_editar, name='direccion_editar'),
    path('direccion/<int:usuario_id>/eliminar-direccion/<int:pk>/', views.direccion_eliminar, name='direccion_eliminar'),

    path('usuarios/<int:usuario_id>/registrar-perfil/', views.registrar_perfil, name='registrar_perfil'),

    path('rol/', views.rol_lista, name='rol_lista'),
    path('rol/crear/', views.rol_crear, name='rol_crear'),
    path('rol/editar/<int:pk>/', views.rol_actualizar, name='rol_actualizar'),
    path('rol/eliminar/<int:pk>/', views.rol_eliminar, name='rol_eliminar'),

    path('bitacora/', views.bitacora_lista, name='bitacora_lista'),
    path('bitacora/crear/', views.bitacora_crear, name='bitacora_crear'),
    path('bitacora/editar/<int:pk>/', views.bitacora_editar, name='bitacora_editar'),
    path('bitacora/eliminar/<int:pk>/', views.bitacora_eliminar, name='bitacora_eliminar'),

    path('bitacora/historial/', views.historial_bitacora, name='historial_bitacora'),
    

]