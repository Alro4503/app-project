import os
import json
import re
from src.auth.user import User

USERS_FILE = "data/users.json"


def createUser(name, surname, email, password):
    return User(name, surname, email, password)


def validar_nombre(nombre):
    """Valida nombre o apellido"""
    if not nombre:
        return False, "Campo obligatorio"
    name_pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{1,25}$'
    if not re.match(name_pattern, nombre):
        return False, "Solo letras y espacios (máx 25 caracteres)"
    return True, ""


def validar_email(email):
    """Valida email"""
    if not email:
        return False, "Campo obligatorio"
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        return False, "Formato inválido (ej: usuario@mail.com)"
    return True, ""


def validar_password(password):
    """Valida contraseña"""
    if not password:
        return False, "Campo obligatorio"
    
    errores = []
    if len(password) < 8:
        errores.append("8 caracteres")
    if not re.search(r'[A-Z]', password):
        errores.append("1 mayúscula")
    if not re.search(r'[0-9]', password):
        errores.append("1 número")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/]', password):
        errores.append("1 especial")
    
    if errores:
        return False, "Falta: " + ", ".join(errores)
    return True, ""


def validateInputs(name, surname, email, password):
    """Validación completa para consola"""
    if not name or not surname or not email or not password:
        print("✘ Todos los campos son obligatorios.")
        return False
    
    valido_nombre, msg_nombre = validar_nombre(name)
    if not valido_nombre:
        print(f"✘ Nombre: {msg_nombre}")
        return False
    
    valido_apellido, msg_apellido = validar_nombre(surname)
    if not valido_apellido:
        print(f"✘ Apellido: {msg_apellido}")
        return False
    
    valido_email, msg_email = validar_email(email)
    if not valido_email:
        print(f"✘ Email: {msg_email}")
        return False
    
    valido_pass, msg_pass = validar_password(password)
    if not valido_pass:
        print(f"✘ Contraseña: {msg_pass}")
        return False
    
    return True


def inputUser(nameEntry, surnameEntry, emailEntry, passwordEntry):
    name = input(nameEntry + " : ").strip()
    surname = input(surnameEntry + " : ").strip()
    email = input(emailEntry + " : ").strip()
    password = input(passwordEntry + " : ").strip()

    if validateInputs(name, surname, email, password):
        return createUser(name, surname, email, password)
    return False


def validateUser(user, password):
    return user.password == password


def userExists(email, password):
    usuarios = cargar_usuarios()
    for usuario in usuarios:
        if usuario.get("email") == email and usuario.get("password") == password:
            return True, usuario
    return False, None


def removeUser(email):
    usuarios = cargar_usuarios()
    nuevos = [u for u in usuarios if u.get("email") != email]
    guardar_usuarios(nuevos)
    return True


def guardar_usuarios(usuarios, ruta=USERS_FILE):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as file:
        json.dump(usuarios, file, indent=4, ensure_ascii=False)


def cargar_usuarios(ruta=USERS_FILE):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)
        return []

    with open(ruta, "r", encoding="utf-8") as file:
        return json.load(file)