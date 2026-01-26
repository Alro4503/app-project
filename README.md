# ⚡Pokémon Toolkit & Z-A Manager

    Una herramienta integral desarrollada en Python para entrenadores Pokémon. Permite gestionar usuarios, consultar datos técnicos mediante la PokeAPI y realizar web scraping para obtener información estratégica sobre movimientos, información Pokemon y megaevoluciones.

# Miembros

    Sergi Fernández Fernández
    Álvaro Rodríguez Líndez


# Características Principales

    Sistema de Autenticación: Registro e inicio de sesión con validaciones de seguridad (email, complejidad de contraseña).

    Consulta de PokeAPI: Obtención de estadísticas base, tipos, habilidades y sprites en tiempo real.

    Web Scraping Avanzado:

    Extracción de mejores movimientos (Ofensivos/Defensivos) desde Pokemon Gameinfo.

    Clasificación y consulta de Megaevoluciones.

 # Interfaz

    Interfaz Dual: Soporte para ejecución en Terminal (CLI) e Interfaz Gráfica de Usuario (GUI) con Tkinter.

# Gestión de Datos
    
    Almacenamiento local de usuarios en JSON y exportación de datos en CSV.

# Estructura del Proyecto

    APP-PROJECT-MAIN/
    │
    ├── .venv/
    │
    ├── data/
    │   ├── megaevoluciones_general.csv
    │   ├── megaevoluciones_luminaila.csv
    │   ├── moveset_pokemon_6.csv
    │   └── users.json
    │
    ├── src/
    │   ├── auth/
    │   │   ├── __pycache__/
    │   │   ├── __init__.py
    │   │   ├── login.py
    │   │   ├── registrerUser.py
    │   │   └── user.py
    │   │
    │   ├── scraping/
    │   │   ├── __pycache__/
    │   │   ├── __init__.py
    │   │   ├── pokemon_api.py
    │   │   ├── scrape_pokemon_go.py
    │   │   ├── scrape_pokemon_za.py
    │   │   └── ver_clasificacion.py
    │   │
    │   ├── main_gui.py
    │   └── main.py
    │
    ├── README.md
    └── requirements.txt


# Instalación y Configuración

    1. Clonar repositorio
    2. Instalar dependencias: Asegúrate de tener Python 3.x instalado. Luego, ejecuta:
        cd pokemon-toolkit
        pip install -r requirements.txt
# Uso
    · Versión de Consola (CLI):

        python main.py

    · Versión Gráfica (GUI)

        python main_gui.py


# Tecnologías Implementadas

    Lenguaje: Python 3.12+

    Librerías de Scraping: BeautifulSoup4, Requests, lxml.

    Procesamiento de Datos: Pandas.

    Interfaz Gráfica: Tkinter, Pillow (para renderizado de imágenes/sprites).

    API Externa: PokeAPI.

# Notas de Seguridad

    Las contraseñas se validan bajo criterios de: mínimo 8 caracteres, una mayúscula, un número y un carácter especial.

    El sistema utiliza un archivo users.json local. No incluir este archivo en commits públicos si contiene datos reales.

