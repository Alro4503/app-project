from threading import Thread
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from bs4 import BeautifulSoup
import requests
import time
from src.auth.login import login
from src.auth.registrerUser import cargar_usuarios, guardar_usuarios, validateInputs, userExists, createUser

class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Z-A Manager")
        self.root.geometry("450x550")
        self.usuario_actual = None
        self.container = tk.Frame(self.root, padx=30, pady=30)
        self.container.pack(expand=True, fill="both")
        self.mostrar_menu_invitado()

    def limpiar_pantalla(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_menu_invitado(self):
        self.limpiar_pantalla()
        tk.Label(self.container, text="POKÉMON TOOLKIT", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Button(self.container, text="Iniciar Sesión", width=20, command=self.vista_login, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.container, text="Registrarse", width=20, command=self.vista_registro, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self.container, text="Salir", width=20, command=self.root.quit).pack(pady=10)

    def vista_login(self):
        self.limpiar_pantalla()
        tk.Label(self.container, text="Acceso", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.container, text="Email:").pack()
        ent_email = tk.Entry(self.container, width=30)
        ent_email.pack()
        tk.Label(self.container, text="Contraseña:").pack()
        ent_pass = tk.Entry(self.container, show="*", width=30)
        ent_pass.pack()

        def ejecutar_login():
            user = login(ent_email.get(), ent_pass.get())
            if user:
                self.usuario_actual = user
                self.mostrar_menu_autenticado()
            else:
                messagebox.showerror("Error", "Credenciales inválidas")

        tk.Button(self.container, text="Entrar", command=ejecutar_login, bg="#4CAF50", fg="white").pack(pady=20)
        tk.Button(self.container, text="Volver", command=self.mostrar_menu_invitado).pack()

    def vista_registro(self):
        self.limpiar_pantalla()
        tk.Label(self.container, text="Nuevo Usuario", font=("Arial", 14)).pack(pady=10)
        fields = {}
        for label in ["Nombre", "Apellido", "Email", "Contraseña"]:
            tk.Label(self.container, text=f"{label}:").pack()
            ent = tk.Entry(self.container, width=30, show="*" if label == "Contraseña" else "")
            ent.pack()
            fields[label] = ent

        def ejecutar_registro():
            n, a, e, p = fields["Nombre"].get(), fields["Apellido"].get(), fields["Email"].get(), fields["Contraseña"].get()
            if userExists(e, p)[0]:
                messagebox.showwarning("Aviso", "El usuario ya existe")
                return
            if validateInputs(n, a, e, p):
                usuarios = cargar_usuarios()
                nuevo = createUser(n, a, e, p)
                usuarios.append(nuevo.to_dict())
                guardar_usuarios(usuarios)
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                self.mostrar_menu_invitado()
            else:
                messagebox.showerror("Error", "Datos inválidos (Revisa el formato)")

        tk.Button(self.container, text="Registrar", command=ejecutar_registro, bg="#2196F3", fg="white").pack(pady=20)
        tk.Button(self.container, text="Volver", command=self.mostrar_menu_invitado).pack()


    def mostrar_menu_autenticado(self):
        self.limpiar_pantalla()
        tk.Label(self.container, text=f"Panel de Control - {self.usuario_actual['name']}", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(
            self.container, 
            text="📊 Ver Clasificación Megas", 
            command=self.ver_clasificacion, 
            width=30, pady=10, bg="#607D8B", fg="white"
        ).pack(pady=10)

        tk.Button(
            self.container, 
            text="Ejecutar web scraping de Pokémon Z-A", 
            command=self.run_scraping_popup, 
            width=30
        ).pack(pady=5)

        tk.Button(self.container, text="Consultar Mejores Movimientos", command=self.pedir_numero_pokedex, width=30).pack(pady=5)
        tk.Button(self.container, text="Cerrar sesión", command=self.logout, width=30).pack(pady=5)

    def ver_clasificacion(self):
        from src.scraping.ver_clasificacion import leer_clasificacion
        df = leer_clasificacion()
        if df is not None:
            mostrar_tabla_gui(df)

    def run_scraping_popup(self):
        popup = tk.Toplevel()
        popup.title("Scraping Pokémon Z-A")
        popup.geometry("400x150")
        tk.Label(popup, text="Ejecutando web scraping de Pokémon Z-A...", font=("Arial", 12)).pack(pady=20)
        status_label = tk.Label(popup, text="Iniciando...", font=("Arial", 10))
        status_label.pack(pady=10)

        def scraping_task():
            try:
                from src.scraping.scrape_pokemon_za import main as scrape_main
                status_label.config(text="Procesando...")
                scrape_main()
                status_label.config(text="¡Scraping completado!")
                messagebox.showinfo("Éxito", "Scraping completado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")
            finally:
                popup.destroy()

        Thread(target=scraping_task, daemon=True).start()

    def logout(self):
        self.usuario_actual = None
        self.mostrar_menu_invitado()


    def pedir_numero_pokedex(self):
        """Abre un popup para introducir el número de Pokédex y lanza el scraping"""
        pokedex_number = simpledialog.askstring("Número de Pokédex", "Introduce el número de Pokédex del Pokémon:", parent=self.root)
        if pokedex_number:
            Thread(target=self.scraping_movimientos, args=(pokedex_number,), daemon=True).start()

    def scraping_movimientos(self, pokedex_number):
        """Scraping de movimientos y muestra en ventana Treeview"""
        popup = tk.Toplevel(self.root)
        popup.title("Consultando movimientos...")
        popup.geometry("400x100")
        tk.Label(popup, text=f"Consultando movimientos del Pokémon #{pokedex_number}...", font=("Arial", 12)).pack(pady=20)

        try:
            html = self.fetch_html(pokedex_number)
            soup = BeautifulSoup(html, "lxml")
            nombre = self.parse_pokemon_name(soup)
            movimientos = self.parse_movesets(soup)
            popup.destroy()
            self.mostrar_tabla_movimientos(nombre, pokedex_number, movimientos)
        except Exception as e:
            popup.destroy()
            messagebox.showerror("Error", f"No se pudieron obtener los movimientos: {e}")

    # ----------------- FUNCIONES DE SCRAPING -----------------
    def fetch_html(self, pokedex_number):
        url = f"https://pokemon.gameinfo.io/en/pokemon/{pokedex_number}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        time.sleep(1)
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text

    def parse_pokemon_name(self, soup):
        title_tag = soup.find("h1")
        if title_tag:
            return title_tag.text.strip()
        return "Desconocido"

    def parse_movesets(self, soup):
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

    # ----------------- VENTANA DE RESULTADOS -----------------
    def mostrar_tabla_movimientos(self, nombre, pokedex_number, datos):
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Mejores Movimientos - {nombre} (#{pokedex_number})")
        ventana.geometry("600x400")

        tree = ttk.Treeview(ventana, columns=["Categoría", "Movimiento", "Tipo"], show="headings")
        for col in ["Categoría", "Movimiento", "Tipo"]:
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor="center")

        for mov in datos:
            tree.insert("", "end", values=[mov["Categoría"], mov["Movimiento"], mov["Tipo"]])

        tree.pack(expand=True, fill="both")


def mostrar_tabla_gui(df):
    if df is None or df.empty:
        messagebox.showwarning("Sin datos", "No hay datos para mostrar.")
        return
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
