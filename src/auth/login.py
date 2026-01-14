from src.auth.registrerUser import cargar_usuarios, userExists


def login(gui_email=None, gui_password=None):

    if gui_email is not None and gui_password is not None:
        email = gui_email.strip()
        password = gui_password.strip()
    else:
        print("\n=== Iniciar Sesión ===")
        email = input("Email: ").strip()
        password = input("Contraseña: ").strip()
    
    if not email or not password:
        return None
    
    existe, usuario = userExists(email, password)
    
    if existe:
        return usuario
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