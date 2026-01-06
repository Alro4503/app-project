import sys
from src.auth.registrerUser import cargar_usuarios, userExists, createUser, validateInputs, guardar_usuarios
from src.auth.login import login, verificar_sesion_activa, cerrar_sesion
from src.scraping.scrape_pokemon_za import main as scrape_main
from src.scraping.ver_clasificacion import main as ver_clasificacion_main


def registrar_usuario():
    """Registra un nuevo usuario en el sistema."""
    usuarios = cargar_usuarios()

    print("\n=== Registro de Usuario ===")

    name = input("Nombre: ").strip()
    surname = input("Apellido: ").strip()
    email = input("Email: ").strip()
    password = input("Contraseña: ").strip()

    user_exist = userExists(email, password)

    if user_exist[0]:
        print("✘ El usuario ya existe. Intenta con otro email.")
        return 
    
    if not validateInputs(name, surname, email, password):
        print("✘ Datos inválidos. Asegúrate de completar todos los campos correctamente.")
        return 
    
    nuevo_usuario = createUser(name, surname, email, password)

    # Convertir el objeto User a diccionario antes de guardar
    usuarios.append(nuevo_usuario.to_dict())
    guardar_usuarios(usuarios)

    print("✔ Usuario registrado con éxito.")


def menu_invitado():
    """Menú para usuarios no autenticados."""
    while True:
        print("\n=== Menú Principal ===")
        print("1. Iniciar sesión")
        print("2. Registrar nuevo usuario")
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            usuario = login()
            if usuario:
                return usuario
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            print("Saliendo...")
            sys.exit(0)
        else:
            print("Opción no válida, intenta de nuevo.")


def menu_usuario_autenticado(usuario):
    """Menú para usuarios autenticados."""
    while True:
        print("\n=== Menú Principal ===")
        print("1. Ver clasificación de Megaevoluciones")
        print("2. Ejecutar web scraping de Pokémon")
        print("3. Cerrar sesión")
        print("4. Salir")
        
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            ver_clasificacion_main()
        elif opcion == "2":
            scrape_main()
        elif opcion == "3":
            cerrar_sesion()
            return None
        elif opcion == "4":
            print("Saliendo...")
            sys.exit(0)
        else:
            print("Opción no válida, intenta de nuevo.")


def main():
    """Punto de entrada principal de la aplicación."""
    usuario_activo = None
    
    while True:
        if not verificar_sesion_activa(usuario_activo):
            usuario_activo = menu_invitado()
        else:
            usuario_activo = menu_usuario_autenticado(usuario_activo)


if __name__ == "__main__":
    main()