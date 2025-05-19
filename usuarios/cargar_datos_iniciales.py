from usuarios.models import Rol, Estado

roles = [
    ('Cliente', 'Puede hacer pedidos y ver su historial.'),
    ('Empleado', 'Gestiona productos, pedidos y atención al cliente.'),
    ('Administrador', 'Control total del sistema.')
]

for nombre, descripcion in roles:
    Rol.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})


estados = [
    ('Activo', 'Usuario activo con acceso al sistema.'),
    ('Inactivo', 'Usuario desactivado temporalmente.'),
    ('Bloqueado', 'Usuario restringido por seguridad u otras razones.')
]

for nombre, descripcion in estados:
    Estado.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})

print("✅ Roles y estados iniciales cargados correctamente.")
