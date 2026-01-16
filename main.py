import sys
from src.auth.registrerUser import cargar_usuarios, userExists, createUser, validateInputs, guardar_usuarios
from src.auth.login import login, verificar_sesion_activa, cerrar_sesion
from src.scraping.scrape_pokemon_za import main as scrape_main
from src.scraping.ver_clasificacion import main as ver_clasificacion_main
from src.scraping.scrape_pokemon_go import main as scrape_movimientos_main
from src.scraping.pokemon_api import obtener_info_api

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
        print("✘ El usuario ya existe.")
        return 
    
    if not validateInputs(name, surname, email, password):
        print("✘ Datos inválidos.")
        return 
    
    nuevo_usuario = createUser(name, surname, email, password)
    usuarios.append(nuevo_usuario.to_dict())
    guardar_usuarios(usuarios)
    print("✔ Usuario registrado con éxito.")

def menu_invitado():
    """Menú para usuarios no identificados."""
    while True:
        print("\n=== Bienvenido a Pokémon Tool ===")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            usuario = login()
            if usuario:
                print(f"✔ Bienvenido, {usuario.get('name')}!")
                return usuario
            else:
                print("✘ Error en el inicio de sesión.")
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            sys.exit(0)
        else:
            print("Opción no válida.")

def menu_usuario_autenticado(usuario):
    """Menú para usuarios autenticados."""
    while True:
        print("\n=== Menú de Herramientas Pokémon ===")
        print(f"Usuario: {usuario.get('name', 'Entrenador')}")
        print("-" * 30)
        print("1. Ver clasificación de Megaevoluciones")
        print("2. Ejecutar web scraping de Pokémon Z-A")
        print("3. Consultar Mejores Movimientos")
        print("4. Consultar PokeAPI (Datos Generales)")
        print("5. Cerrar sesión")
        print("6. Salir")
        
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            ver_clasificacion_main()
        elif opcion == "2":
            scrape_main()
        elif opcion == "3":
            scrape_movimientos_main()
        elif opcion == "4":
            nombre = input("Introduce nombre o ID del Pokémon: ")
            info = obtener_info_api(nombre)
            if info:
                print(f"\n--- {info['nombre']} (#{info['id']}) ---")
                print(f"Tipos: {info['tipos']}")
                print(f"Stats: {info['stats']}")
            else:
                print("✘ No se encontró el Pokémon.")
        elif opcion == "5":
            cerrar_sesion()
            return None
        elif opcion == "6":
            sys.exit(0)
        else:
            print("Opción no válida.")

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