from django.shortcuts import render, redirect, get_object_or_404
from .forms.form_usuario import UsuarioForm
from .forms.form_perfil import PerfilForm
from .forms.form_direccion import DireccionForm
from .forms.form_rol import RolForm
from .forms.form_Bitacora import BitacoraActividadForm
from .models import Usuario, Direccion, Perfil, Rol, BitacoraActividad
from .models import BitacoraActividad
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.hashers import check_password



def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def registrar_usuario(request):
    if request.session.get('usuario_rol') != 'Administrador':
        messages.error(request, 'No tienes permisos para registrar usuarios.')
        return redirect('lista_usuarios')
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'registrar_usuario.html', {'form': form, 'editar': False})

def editar_usuario(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            usuario.nombre = data['nombre']
            usuario.apellido = data['apellido']
            usuario.numero_documento = data['numero_documento']
            usuario.correo = data['correo']
            usuario.telefono = data['telefono']
            usuario.contrasena = data['contrasena']
            usuario.rol = data['rol']
            usuario.estado = data['estado']
            usuario.save()

            registrar_actividad(
                usuario=usuario,
                accion='Edición de usuario',
                request=request,
                descripcion=f'Se editaron los datos del usuario {usuario.nombre} {usuario.apellido}'
            )
            return redirect('lista_usuarios')
    else:
        datos_iniciales = {
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'numero_documento': usuario.numero_documento,
            'correo': usuario.correo,
            'telefono': usuario.telefono,
            'rol': usuario.rol,
            'estado': usuario.estado,
        }
        form = UsuarioForm(initial=datos_iniciales)
    
    return render(request, 'registrar_usuario.html', {'form': form, 'usuario': usuario, 'editar': True})

def eliminar_usuario(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    if request.method == "POST":
        # Obtener Usuario según correo del usuario autenticado (request.user)
        try:
            usuario_actual = Usuario.objects.get(correo=request.user.email)
        except Usuario.DoesNotExist:
            # Manejar caso si no se encuentra, tal vez asignar None o manejar error
            usuario_actual = None
        
        if usuario_actual:
            BitacoraActividad.objects.create(
                usuario=usuario_actual,
                accion=f'Eliminó al usuario: {usuario.nombre} {usuario.apellido} (ID {usuario.id})',
                request= request,
                descripcion='Se eliminó un usuario del sistema.'
            )

        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})



def direccion_lista(request, usuario_id):
    usuario = Usuario.objects.get(pk=usuario_id)
    direcciones = Direccion.objects.filter(usuario=usuario)
    return render(request, 'direccion_lista.html', {
        'usuario': usuario,
        'direcciones': direcciones
    })

def direccion_crear(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = Direccion(
                usuario=usuario,
                direccion=form.cleaned_data['direccion'],
                barrio=form.cleaned_data['barrio'],
                ciudad=form.cleaned_data['ciudad'],
                principal=form.cleaned_data.get('principal', False)
            )
            direccion.save()
            
            registrar_actividad(
                usuario=usuario,
                accion='Crear dirección',
                descripcion=f'Dirección creada: {direccion.direccion}',
                request=request
            )
            return redirect('direccion_lista', usuario_id=usuario.id)
    else:
        form = DireccionForm()

    return render(request, 'direccion_form.html', {
        'form': form,
        'usuario': usuario
    })

def direccion_editar(request, usuario_id, pk):
    direccion = get_object_or_404(Direccion, pk=pk, usuario_id=usuario_id)
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            form.update(direccion)
            registrar_actividad(
                usuario=direccion.usuario,
                accion='Editar dirección',
                descripcion=f'Dirección editada: {direccion.direccion}',
                request=request
            )
            return redirect('direccion_lista', usuario_id=direccion.usuario.id)
    else:
        form = DireccionForm(initial={
            'usuario': direccion.usuario,
            'direccion': direccion.direccion,
            'barrio': direccion.barrio,
            'ciudad': direccion.ciudad,
            'principal': direccion.principal
        })
    return render(request, 'direccion_form.html', {'form': form, 'usuario': direccion.usuario})

def direccion_eliminar(request, usuario_id, pk):
    direccion = get_object_or_404(Direccion, pk=pk, usuario_id=usuario_id)
    if request.method == 'POST':
        direccion.delete()
        registrar_actividad(
            usuario=direccion.usuario,
            accion='Eliminar dirección',
            descripcion=f'Dirección eliminada: {direccion.direccion}',
            request=request
        )
        return redirect('direccion_lista', usuario_id=usuario_id)
    return render(request, 'direccion_confirmar_eliminar.html', {'direccion': direccion, 'usuario_id': usuario_id})

def registrar_perfil(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
            return redirect('detalle_usuario', usuario_id=usuario.id)
    else:
        form = PerfilForm()

    return render(request, 'registrar_perfil.html', {'form': form, 'usuario': usuario})

def rol_crear(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rol_lista')
    else:
        form = RolForm()
    return render(request, 'rol_form.html', {'form': form})

def rol_lista(request):
    roles = Rol.objects.all()
    return render(request, 'rol_lista.html', {'roles': roles})

def rol_actualizar(request, pk):
    rol = Rol.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            rol.nombre = form.cleaned_data['nombre']
            rol.descripcion = form.cleaned_data['descripcion']
            rol.save()
            return redirect('rol_lista')
    else:
        datos_iniciales = {
            'nombre': rol.nombre,
            'descripcion': rol.descripcion,
        }
        form = RolForm(initial=datos_iniciales)
    
    return render(request, 'rol_form.html', {'form': form, 'editar': True})

def rol_eliminar(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    if request.method == 'POST':
        rol.delete()
        return redirect('rol_lista')
    return render(request, 'rol_confirmar_eliminacion.html', {'rol': rol})


def bitacora_lista(request):
    bitacoras = BitacoraActividad.objects.select_related('usuario').order_by('-fecha')
    return render(request, 'bitacora_lista.html', {'bitacoras': bitacoras})

def bitacora_crear(request):
    if request.method == 'POST':
        form = BitacoraActividadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bitacora_lista')
    else:
        form = BitacoraActividadForm()
    return render(request, 'bitacora_form.html', {'form': form})

def bitacora_editar(request, pk):
    bitacora = get_object_or_404(BitacoraActividad, pk=pk)
    if request.method == 'POST':
        form = BitacoraActividadForm(request.POST, instance=bitacora)
        if form.is_valid():
            form.save()
            return redirect('bitacora_lista')
    else:
        form = BitacoraActividadForm(instance=bitacora)
    return render(request, 'bitacora_form.html', {'form': form})

def bitacora_eliminar(request, pk):
    bitacora = get_object_or_404(BitacoraActividad, pk=pk)
    if request.method == 'POST':
        bitacora.delete()
        return redirect('bitacora_lista')
    return render(request, 'bitacora_confirmar_eliminar.html', {'bitacora': bitacora})



def registrar_actividad(usuario, accion, request=None, descripcion=None):
    ip = request.META.get('REMOTE_ADDR') if request else None
    BitacoraActividad.objects.create(
        usuario=usuario,
        accion=accion,
        ip=ip,
        descripcion=descripcion
    )


def historial_bitacora (request):
    rol = request.session.get('usuario_rol')
    
    if rol != 'Administrador':
        messages.error(request, 'No tienes permisos para ver la bitácora.')
        return redirect('lista_usuarios')
    
    bitacoras = BitacoraActividad.objects.select_related('usuario', 'usuario__rol').order_by('-fecha')
    return render(request, 'bitacora/historial.html', {'bitacoras': bitacoras})



def login_usuario(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        
        try:
            usuario = Usuario.objects.get(correo=correo)
            if check_password(contrasena, usuario.contrasena):
                if usuario.estado.nombre == 'Inactivo':
                    messages.error(request, 'Tu cuenta está inactiva.')
                    return redirect('login_usuario')
                
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_rol'] = usuario.rol.nombre
                messages.success(request, f'¡Bienvenido, {usuario.nombre}!')
                return redirect('lista_usuarios') 
            else:
                messages.error(request, 'Correo o contraseña incorrectos.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos.')
    
    return render(request, 'login.html')


def logout_usuario(request):
    request.session.flush()
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login_usuario')

