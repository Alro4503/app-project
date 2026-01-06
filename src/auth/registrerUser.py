import os
import json
import re
from src.auth.user import User

USERS_FILE = "data/users.json"


def createUser(name, surname, email, password):
    return User(name, surname, email, password)


def validateInputs(name, surname, email, password):

    # Validar que los campos no estén vacíos
    if not name or not surname or not email or not password:
        print("✘ Todos los campos son obligatorios.")
        return False
    
    # Validar nombre y apellido: solo letras y espacios, máximo 25 caracteres
    name_pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{1,25}$'
    if not re.match(name_pattern, name):
        print("✘ El nombre debe contener solo letras y espacios (máximo 25 caracteres).")
        return False
    
    if not re.match(name_pattern, surname):
        print("✘ El apellido debe contener solo letras y espacios (máximo 25 caracteres).")
        return False
    
    # Validar email: texto@texto.texto
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        print("✘ El email no tiene un formato válido.")
        return False
    
    # Validar contraseña: mínimo 8 caracteres, 1 mayúscula, 1 número, 1 carácter especial
    if len(password) < 8:
        print("✘ La contraseña debe tener al menos 8 caracteres.")
        return False
    
    if not re.search(r'[A-Z]', password):
        print("✘ La contraseña debe contener al menos una letra mayúscula.")
        return False
    
    if not re.search(r'[0-9]', password):
        print("✘ La contraseña debe contener al menos un número.")
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/]', password):
        print("✘ La contraseña debe contener al menos un carácter especial (!@#$%^&*...).")
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
    # Crear directorio data si no existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as file:
        json.dump(usuarios, file, indent=4, ensure_ascii=False)


def cargar_usuarios(ruta=USERS_FILE):
    # Crear directorio data si no existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)
        return []

    with open(ruta, "r", encoding="utf-8") as file:
        return json.load(file)