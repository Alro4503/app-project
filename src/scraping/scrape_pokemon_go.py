import requests
from bs4 import BeautifulSoup
import time

def fetch_html(pokedex_number):
    url = f"https://pokemon.gameinfo.io/en/pokemon/{pokedex_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    time.sleep(1) 
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.text

def parse_pokemon_name(soup):
    # Buscamos el h1 o el h2 principal que contiene el nombre
    # En esta web, el nombre suele estar en un h1 dentro del header
    title_tag = soup.find("h1")
    if title_tag:
        return title_tag.text.strip()
    return "Desconocido"

def parse_movesets(soup):
    moves_data = []
    headers = soup.find_all("h3", class_="text-center")
    
    for h3 in headers:
        category = h3.text.strip()
        if category not in ["Offense", "Defense"]:
            continue
            
        container = h3.find_next_sibling("div")
        if container:
            move_links = container.select("div.truncate.grow a")
            for link in move_links:
                move_name = link.text.strip()
                move_type = "Unknown"
                span_type = link.find_previous_sibling("span", class_="move-icon")
                if span_type and span_type.has_attr("data-type"):
                    move_type = span_type["data-type"].capitalize()
                
                moves_data.append({
                    "Categoría": category,
                    "Movimiento": move_name,
                    "Tipo": move_type
                })
    return moves_data

def imprimir_tabla(datos, pokedex_id, nombre_pokemon):
    if not datos:
        print(f"\nNo se encontraron movimientos para {nombre_pokemon} (#{pokedex_id}).")
        return

    print("\n" + "="*65)
    print(f"  MEJORES MOVIMIENTOS: {nombre_pokemon.upper()} (#{pokedex_id})")
    print("="*65)
    print(f"{'CATEGORÍA':<15} | {'MOVIMIENTO':<30} | {'TIPO':<10}")
    print("-" * 65)
    
    for m in datos:
        print(f"{m['Categoría']:<15} | {m['Movimiento']:<30} | {m['Tipo']:<10}")
    
    print("="*65)
    print(f"Total encontrados: {len(datos)}\n")

def main():
    print("\n--- CONSULTA DE MOVIMIENTOS EN TIEMPO REAL ---")
    pokedex_id = input("Introduce el número de Pokédex: ")
    
    try:
        html = fetch_html(pokedex_id)
        soup = BeautifulSoup(html, "lxml")
        
        print(f"Buscando información...")
        
        # Extraemos nombre y movimientos
        nombre = parse_pokemon_name(soup)
        datos = parse_movesets(soup)
        
        imprimir_tabla(datos, pokedex_id, nombre)
        
    except Exception as e:
        print(f"Error al obtener datos: {e}")

if __name__ == "__main__":
    main()