import pandas as pd
import os

CSV_FILE = "megaevoluciones_general.csv"

def leer_clasificacion():
    if not os.path.exists(CSV_FILE):
        print(f"Error: No se encuentra el archivo '{CSV_FILE}'")
        print("Ejecuta primero el script de scraping para generar el CSV.")
        return None
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"\nArchivo '{CSV_FILE}' leído correctamente.")
        return df
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def mostrar_tabla(df):
    print("\n" + "="*80)
    print("  CLASIFICACIÓN MEGAS EN POKEMON Z-A")
    print("="*80)
    print()
    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 150)
    pd.set_option('display.max_columns', None)
    
    # Aquí ajusta columnas si sabes sus nombres o déjalo así para mostrar todo:
    print(df.to_string(index=False))
    
    print("="*80)
    print(f"\nTotal de registros: {len(df)}")
    print()


def main():
    print("\nVISUALIZADOR DE DATOS MEGAEVOLUCIONES\n")
    df = leer_clasificacion()
    if df is None or df.empty:
        return
    mostrar_tabla(df)
    print("Datos leídos desde:", CSV_FILE)
    print()

if __name__ == "__main__":
    main()
