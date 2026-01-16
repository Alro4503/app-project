from threading import Thread
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from src.auth.login import login
from src.auth.registrerUser import (cargar_usuarios, guardar_usuarios, userExists, 
                                     createUser, validar_nombre, validar_email, validar_password)
from src.scraping.pokemon_api import obtener_info_api, descargar_sprite

class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Z-A Manager")
        self.root.geometry("450x650")
        self.usuario_actual = None
        self.container = tk.Frame(self.root, padx=30, pady=30)
        self.container.pack(expand=True, fill="both")
        self.mostrar_menu_invitado()

    def limpiar_pantalla(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_menu_invitado(self):
        self.limpiar_pantalla()
        tk.Label(self.container, text="⚡ POKÉMON TOOLKIT ⚡", font=("Segoe UI Emoji", 18, "bold")).pack(pady=20)
        tk.Button(self.container, text="🔑  Iniciar Sesión", width=20, command=self.vista_login, 
                  bg="#4CAF50", fg="white", font=("Segoe UI Emoji", 10, "bold"), pady=8).pack(pady=10)
        tk.Button(self.container, text="✨  Registrarse", width=20, command=self.vista_registro, 
                  bg="#2196F3", fg="white", font=("Segoe UI Emoji", 10, "bold"), pady=8).pack(pady=10)
        tk.Button(self.container, text="❌  Salir", width=20, command=self.root.quit,
                  bg="#f44336", fg="white", font=("Segoe UI Emoji", 10, "bold"), pady=8).pack(pady=10)

    def crear_campo(self, parent, label, show=None):
        """Crea campo con validación en tiempo real"""
        frame = tk.Frame(parent)
        frame.pack(pady=5)
        tk.Label(frame, text=label, font=("Arial", 10, "bold")).pack(anchor="w")
        
        entry_frame = tk.Frame(frame)
        entry_frame.pack()
        entry = tk.Entry(entry_frame, width=30, show=show if show else "")
        entry.pack(side="left")
        
        val_label = tk.Label(entry_frame, text="", font=("Arial", 14), width=2)
        val_label.pack(side="left", padx=5)
        
        err_label = tk.Label(frame, text="", font=("Arial", 8), fg="#f44336", wraplength=280)
        err_label.pack()
        
        return entry, val_label, err_label

    def validar_campo(self, valor, validador, val_label, err_label):
        """Aplica validación y actualiza UI"""
        if not valor:
            val_label.config(text="")
            err_label.config(text="")
            return False
        valido, msg = validador(valor)
        if valido:
            val_label.config(text="✓", fg="#4CAF50")
            err_label.config(text="")
        else:
            val_label.config(text="✗", fg="#f44336")
            err_label.config(text=msg)
        return valido

    def vista_login(self):
        self.limpiar_pantalla()
        tk.Label(self.container, text="🔑 Acceso", font=("Segoe UI Emoji", 14, "bold")).pack(pady=10)
        
        ent_email, val_email, err_email = self.crear_campo(self.container, "📧 Email:")
        ent_pass, val_pass, err_pass = self.crear_campo(self.container, "🔒 Contraseña:", "*")
        
        ent_email.bind('<KeyRelease>', lambda e: self.validar_campo(ent_email.get(), validar_email, val_email, err_email))
        ent_pass.bind('<KeyRelease>', lambda e: val_pass.config(text="🔒" if ent_pass.get() else ""))

        def ejecutar_login():
            email, password = ent_email.get().strip(), ent_pass.get().strip()
            if not email or not password:
                messagebox.showerror("Error", "Completa todos los campos")
                return
            
            user = login(email, password)
            if user:
                self.usuario_actual = user
                self.mostrar_menu_autenticado()
            else:
                messagebox.showerror("Error", "Credenciales inválidas")

        tk.Button(self.container, text="🚀  Entrar", command=ejecutar_login, bg="#4CAF50", 
                  fg="white", font=("Segoe UI Emoji", 10, "bold"), width=20, pady=8).pack(pady=20)
        tk.Button(self.container, text="⬅️  Volver", command=self.mostrar_menu_invitado,
                  width=20, pady=8).pack()

    def vista_registro(self):
        self.limpiar_pantalla()
        tk.Label(self.container, text="✨ Nuevo Usuario", font=("Segoe UI Emoji", 14, "bold")).pack(pady=10)
        
        ent_name, val_name, err_name = self.crear_campo(self.container, "👤 Nombre:")
        ent_surname, val_surname, err_surname = self.crear_campo(self.container, "👥 Apellido:")
        ent_email, val_email, err_email = self.crear_campo(self.container, "📧 Email:")
        ent_pass, val_pass, err_pass = self.crear_campo(self.container, "🔒 Contraseña:", "*")
        
        ent_name.bind('<KeyRelease>', lambda e: self.validar_campo(ent_name.get(), validar_nombre, val_name, err_name))
        ent_surname.bind('<KeyRelease>', lambda e: self.validar_campo(ent_surname.get(), validar_nombre, val_surname, err_surname))
        ent_email.bind('<KeyRelease>', lambda e: self.validar_campo(ent_email.get(), validar_email, val_email, err_email))
        ent_pass.bind('<KeyRelease>', lambda e: self.validar_campo(ent_pass.get(), validar_password, val_pass, err_pass))

        def ejecutar_registro():
            n, a, e, p = ent_name.get().strip(), ent_surname.get().strip(), ent_email.get().strip(), ent_pass.get().strip()
            if not all([n, a, e, p]):
                messagebox.showerror("Error", "Completa todos los campos")
                return
            
            usuarios = cargar_usuarios()
            nuevo = createUser(n, a, e, p)
            usuarios.append(nuevo.to_dict())
            guardar_usuarios(usuarios)
            messagebox.showinfo("Éxito", "Usuario registrado")
            self.mostrar_menu_invitado()

        tk.Button(self.container, text="✅  Registrar", command=ejecutar_registro, bg="#2196F3", 
                  fg="white", font=("Segoe UI Emoji", 10, "bold"), width=20, pady=8).pack(pady=20)
        tk.Button(self.container, text="⬅️  Volver", command=self.mostrar_menu_invitado,
                  width=20, pady=8).pack()

    def mostrar_menu_autenticado(self):
        self.limpiar_pantalla()
        tk.Label(self.container, text=f"⚡ Panel - {self.usuario_actual['name']}", 
                 font=("Segoe UI Emoji", 14, "bold")).pack(pady=10)

        tk.Button(self.container, text="📊  Ver Clasificación Megas", command=self.ver_clasificacion, 
                  width=30, pady=10, bg="#607D8B", fg="white", font=("Segoe UI Emoji", 10, "bold")).pack(pady=5)
        tk.Button(self.container, text="🌐  Web Scraping Pokémon Z-A", command=self.run_scraping_popup, 
                  width=30, pady=10, bg="#9C27B0", fg="white", font=("Segoe UI Emoji", 10, "bold")).pack(pady=5)
        tk.Button(self.container, text="⚔️  Consultar Mejores Movimientos", command=self.pedir_numero_pokedex, 
                  width=30, pady=10, bg="#FF5722", fg="white", font=("Segoe UI Emoji", 10, "bold")).pack(pady=5)
    
        tk.Button(self.container, text="🔍  Consultar PokeAPI (Info + Sprite)", command=self.vista_pokeapi, 
                  width=30, pady=10, bg="#2196F3", fg="white", font=("Segoe UI Emoji", 10, "bold")).pack(pady=5)

        tk.Button(self.container, text="🚪  Cerrar sesión", command=self.logout, 
                  width=30, pady=10, bg="#f44336", fg="white", font=("Segoe UI Emoji", 10, "bold")).pack(pady=15)

    def vista_pokeapi(self):
        busqueda = simpledialog.askstring("PokeAPI", "Nombre o ID del Pokémon:", parent=self.root)
        if not busqueda: return
        
        info = obtener_info_api(busqueda)
        if not info:
            messagebox.showerror("Error", "No se encontró el Pokémon")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title(f"Datos: {info['nombre']}")
        ventana.geometry("400x550")

        sprite = descargar_sprite(info['sprite_url'])
        if sprite:
            label_img = tk.Label(ventana, image=sprite)
            label_img.image = sprite 
            label_img.pack(pady=10)

        tk.Label(ventana, text=f"{info['nombre']} (#{info['id']})", font=("Arial", 16, "bold")).pack()
        tk.Label(ventana, text=f"Tipos: {', '.join(info['tipos'])}", font=("Arial", 10, "italic")).pack()
        
        detalles_frame = tk.Frame(ventana, pady=10)
        detalles_frame.pack()
        tk.Label(detalles_frame, text=f"Altura: {info['altura']}m | Peso: {info['peso']}kg").pack()
        tk.Label(detalles_frame, text=f"Habilidades: {', '.join(info['habilidades'])}").pack()

        tk.Label(ventana, text="\nESTADÍSTICAS BASE:", font=("Arial", 10, "bold")).pack()
        stats_txt = ""
        for k, v in info['stats'].items():
            stats_txt += f"{k.upper()}: {v}\n"
        tk.Label(ventana, text=stats_txt, justify="left").pack()

    def ver_clasificacion(self):
        from src.scraping.ver_clasificacion import leer_clasificacion
        df = leer_clasificacion()
        if df is not None:
            mostrar_tabla_gui(df)

    def run_scraping_popup(self):
        popup = tk.Toplevel()
        popup.title("Scraping Pokémon Z-A")
        popup.geometry("400x150")
        tk.Label(popup, text="Ejecutando web scraping...", font=("Arial", 12)).pack(pady=20)
        status_label = tk.Label(popup, text="Iniciando...", font=("Arial", 10))
        status_label.pack(pady=10)

        def scraping_task():
            try:
                from src.scraping.scrape_pokemon_za import main as scrape_main
                scrape_main()
                messagebox.showinfo("Éxito", "Scraping completado")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")
            finally:
                popup.destroy()

        Thread(target=scraping_task, daemon=True).start()

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Seguro?"):
            self.usuario_actual = None
            self.mostrar_menu_invitado()

    def pedir_numero_pokedex(self):
        pokedex_number = simpledialog.askstring("Número de Pokédex", "Introduce el número:", parent=self.root)
        if pokedex_number:
            if not pokedex_number.isdigit():
                messagebox.showerror("Error", "Debe ser un número válido")
                return
            Thread(target=self.scraping_movimientos, args=(pokedex_number,), daemon=True).start()

    def scraping_movimientos(self, pokedex_number):
        try:
            url = f"https://pokemon.gameinfo.io/en/pokemon/{pokedex_number}"
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            
            nombre = soup.find("h1").text.strip() if soup.find("h1") else "Desconocido"
            
            moves_data = []
            headers_movs = soup.find_all("h3", class_="text-center")
            for h3 in headers_movs:
                category = h3.text.strip()
                if category not in ["Offense", "Defense"]: continue
                container = h3.find_next_sibling("div")
                if container:
                    links = container.select("div.truncate.grow a")
                    for link in links:
                        moves_data.append({
                            "Categoría": category,
                            "Movimiento": link.text.strip(),
                            "Tipo": "Especial"
                        })
            
            self.mostrar_tabla_movimientos(nombre, pokedex_number, moves_data)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener: {e}")

    def mostrar_tabla_movimientos(self, nombre, pokedex_number, datos):
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Movimientos - {nombre} (#{pokedex_number})")
        ventana.geometry("600x400")

        tree = ttk.Treeview(ventana, columns=["Categoría", "Movimiento", "Tipo"], show="headings")
        for col in ["Categoría", "Movimiento", "Tipo"]:
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor="center")

        for mov in datos:
            tree.insert("", "end", values=[mov["Categoría"], mov["Movimiento"], mov["Tipo"]])

        tree.pack(expand=True, fill="both")

def mostrar_tabla_gui(df):
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title("Clasificación Megaevoluciones")
    ventana_tabla.geometry("800x500")

    frame = tk.Frame(ventana_tabla)
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()