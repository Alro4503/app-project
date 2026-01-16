import requests
from io import BytesIO
from PIL import Image, ImageTk

def obtener_info_api(nombre_o_id):
    """Obtiene datos básicos de un Pokémon desde PokeAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{str(nombre_o_id).lower().strip()}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
        
        info = {
            "nombre": data["name"].capitalize(),
            "id": data["id"],
            "altura": data["height"] / 10,
            "peso": data["weight"] / 10,
            "tipos": [t["type"]["name"].capitalize() for t in data["types"]],
            "habilidades": [h["ability"]["name"].capitalize() for h in data["abilities"]],
            "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
            "sprite_url": data["sprites"]["front_default"]
        }
        return info
    except Exception as e:
        print(f"Error al conectar con PokeAPI: {e}")
        return None

def descargar_sprite(url):
    """Descarga la imagen"""
    try:
        response = requests.get(url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((150, 150), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except:
        return None