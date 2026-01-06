from src.auth.registrerUser import cargar_usuarios, userExists


def login():
    """
    Función para iniciar sesión de usuario.
    Retorna el usuario si el login es exitoso, None en caso contrario.
    """
    print("\n=== Iniciar Sesión ===")
    
    email = input("Email: ").strip()
    password = input("Contraseña: ").strip()
    
    # Validar que los campos no estén vacíos
    if not email or not password:
        print("✘ Por favor, completa todos los campos.")
        return None
    
    # Verificar si el usuario existe
    existe, usuario = userExists(email, password)
    
    if existe:
        print(f"✔ Bienvenido/a, {usuario.get('name')} {usuario.get('surname')}!")
        return usuario
    else:
        print("✘ Credenciales incorrectas. Email o contraseña inválidos.")
        return None


def verificar_sesion_activa(usuario_activo):
    """
    Verifica si hay una sesión activa.
    Retorna True si hay sesión, False en caso contrario.
    """
    return usuario_activo is not None


def cerrar_sesion():
    """
    Cierra la sesión del usuario actual.
    """
    print("\n✔ Sesión cerrada exitosamente.")
    return None