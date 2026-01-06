import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import sys
import time
import os

URL = "https://vandal.elespanol.com/guias/guia-leyendas-pokemon-za-trucos-consejos-y-secretos/pokemon-megaevolucion"

def fetch_html(url, timeout=15):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; educational scraper)"}
    time.sleep(2)
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def save_to_csv(data, filename):
    if not data:
        print("No hay datos para guardar.")
        return
    
    # Crear directorio data si no existe
    filepath = os.path.join("data", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    fieldnames = list(data[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"\nDatos guardados en {filepath}")
    print(f"Total de registros: {len(data)}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def parse_table(soup):
    data = []
    # Buscar tabla por encabezado que contenga "Pokémon Megaevolución"
    table = soup.find("table")
    if not table:
        print("No se encontró tabla de Megaevoluciones")
        return data

    rows = table.find_all("tr")
    for row in rows[1:]:  # Saltar encabezado
        cols = row.find_all("td")
        if len(cols) < 4:
            continue
        nro_pokedex = cols[0].text.strip()
        # Nombre dentro del segundo td, dentro del <b> o <strong> o texto después de la imagen
        name_tag = cols[1].find("b") or cols[1].find("strong")
        if name_tag:
            name = name_tag.text.strip()
        else:
            name = cols[1].text.strip()
        tipo = cols[2].text.strip()
        megapiedra = cols[3].text.strip()
        data.append({
            "Nº Pokédex": nro_pokedex,
            "Mega Pokémon": name,
            "Tipo": tipo,
            "Megapiedra": megapiedra
        })
    return data

def parse_luminalia_section(soup):
    data = []
    # Buscar secciones con Mega Luminalia, podrían estar en <h2>, <h3> o <strong>
    headers = soup.find_all(["h2","h3","strong"])
    for h in headers:
        title = h.text.strip().lower()
        if "mega" in title:
            # Obtener siguiente hermano o lista que contiene datos
            ul = h.find_next_sibling("ul")
            if not ul:
                continue
            details = {"Mega Pokémon": title.title()}  # Nombre en título con mayúsculas
            for li in ul.find_all("li"):
                text = li.text.strip()
                if "nº pokédex luminalia" in text.lower():
                    details["Nº Pokédex Luminalia"] = text.split(":")[-1].strip()
                elif "tipo" in text.lower():
                    details["Tipo"] = text.split(":")[-1].strip()
                elif "megapiedra" in text.lower():
                    details["Megapiedra"] = text.split(":")[-1].strip()
            data.append(details)
    return data

def main():
    print("Extrayendo:", URL)
    try:
        html = fetch_html(URL)
    except Exception as e:
        print("Error al descargar la página:", e)
        sys.exit(1)

    soup = BeautifulSoup(html, "lxml")

    print("Parseando tabla principal de megas...")
    data_general = parse_table(soup)
    print(f"Encontrados {len(data_general)} megas en tabla principal.")

    print("Parseando sección Luminalia...")
    data_luminalia = parse_luminalia_section(soup)
    print(f"Encontrados {len(data_luminalia)} megas en sección Luminalia.")

    # Guardar ambos datos por separado o combinar
    save_to_csv(data_general, "megaevoluciones_general.csv")
    save_to_csv(data_luminalia, "megaevoluciones_luminalia.csv")

if __name__ == "__main__":
    main()