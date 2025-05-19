from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=30, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=255)
    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True)
    estado = models.ForeignKey('Estado', on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk: 
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.numero_documento} - {self.rol}"
    

class Direccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direcciones')
    direccion = models.CharField(max_length=200)
    barrio = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    principal = models.BooleanField(default=False)


class BitacoraActividad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.usuario.nombre} - {self.accion} - {self.fecha}"

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    def __str__(self):
        return f"{self.nombre} - {self.descripcion}" 


class Estado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    def __str__(self):
        return self.nombre


