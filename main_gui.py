from threading import Thread
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from bs4 import BeautifulSoup
import requests
import time
import re
from src.auth.login import login
from src.auth.registrerUser import cargar_usuarios, guardar_usuarios, userExists, createUser

class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Z-A Manager")
        self.root.geometry("500x650")
        self.root.configure(bg="#f0f0f0")
        self.usuario_actual = None
        
        # Colores del tema
        self.COLORS = {
            "primary": "#4CAF50",
            "secondary": "#2196F3",
            "danger": "#f44336",
            "warning": "#ff9800",
            "bg": "#f0f0f0",
            "card": "#ffffff",
            "text": "#333333",
            "success": "#4CAF50",
            "error": "#f44336"
        }
        
        # Iconos de tipos de Pokémon (emoji)
        self.TYPE_ICONS = {
            "fire": "🔥",
            "water": "💧",
            "grass": "🌿",
            "electric": "⚡",
            "ice": "❄️",
            "fighting": "🥊",
            "poison": "☠️",
            "ground": "⛰️",
            "flying": "🕊️",
            "psychic": "🔮",
            "bug": "🐛",
            "rock": "🪨",
            "ghost": "👻",
            "dragon": "🐉",
            "dark": "🌑",
            "steel": "⚙️",
            "fairy": "✨",
            "normal": "⭐",
            "unknown": "❓"
        }
        
        self.container = tk.Frame(self.root, padx=30, pady=30, bg=self.COLORS["bg"])
        self.container.pack(expand=True, fill="both")
        self.mostrar_menu_invitado()

    def limpiar_pantalla(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_menu_invitado(self):
        self.limpiar_pantalla()
        
        # Frame principal centrado
        main_frame = tk.Frame(self.container, bg=self.COLORS["bg"])
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título con emoji
        title_frame = tk.Frame(main_frame, bg=self.COLORS["bg"])
        title_frame.pack(pady=20)
        
        tk.Label(
            title_frame, 
            text="⚡ POKÉMON TOOLKIT ⚡", 
            font=("Segoe UI Emoji", 20, "bold"),
            bg=self.COLORS["bg"],
            fg=self.COLORS["text"]
        ).pack()
        
        tk.Label(
            title_frame,
            text="Gestiona tu equipo Pokémon",
            font=("Arial", 10),
            bg=self.COLORS["bg"],
            fg="#666666"
        ).pack()
        
        # Botones con iconos
        btn_frame = tk.Frame(main_frame, bg=self.COLORS["bg"])
        btn_frame.pack(pady=20)
        
        self.crear_boton_icono(
            btn_frame, 
            "🔑  Iniciar Sesión", 
            self.vista_login, 
            self.COLORS["primary"],
            width=28
        ).pack(pady=10)
        
        self.crear_boton_icono(
            btn_frame,
            "✨  Registrarse",
            self.vista_registro,
            self.COLORS["secondary"],
            width=28
        ).pack(pady=10)
        
        self.crear_boton_icono(
            btn_frame,
            "❌  Salir",
            self.root.quit,
            self.COLORS["danger"],
            width=28
        ).pack(pady=10)

    def crear_boton_icono(self, parent, text, command, bg_color, width=25):
        """Crea un botón estilizado con efecto hover"""
        btn = tk.Button(
            parent,
            text=text,
            width=width,
            command=command,
            bg=bg_color,
            fg="white",
            font=("Segoe UI Emoji", 11, "bold"),  # Fuente que soporta emojis a color
            relief=tk.FLAT,
            cursor="hand2",
            pady=12,
            anchor="center"
        )
        
        # Efecto hover
        def on_enter(e):
            btn['bg'] = self.ajustar_color(bg_color, -20)
        
        def on_leave(e):
            btn['bg'] = bg_color
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def ajustar_color(self, hex_color, ajuste):
        """Ajusta el brillo de un color hex"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, min(255, c + ajuste)) for c in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def crear_campo_validado(self, parent, label_text, show_char=None):
        """Crea un campo de entrada con label y validación visual"""
        frame = tk.Frame(parent, bg=self.COLORS["bg"])
        frame.pack(pady=5)
        
        # Label
        label = tk.Label(
            frame,
            text=label_text,
            font=("Arial", 10, "bold"),
            bg=self.COLORS["bg"],
            fg=self.COLORS["text"],
            anchor="w"
        )
        label.pack(anchor="w")
        
        # Frame para entrada + icono de validación (centrado)
        entry_frame = tk.Frame(frame, bg=self.COLORS["bg"])
        entry_frame.pack()
        
        entry = tk.Entry(
            entry_frame,
            width=28,
            font=("Arial", 11),
            show=show_char if show_char else "",
            relief=tk.SOLID,
            borderwidth=1,
            justify="left"
        )
        entry.pack(side="left", ipady=5)
        
        # Icono de validación
        validation_label = tk.Label(
            entry_frame,
            text="",
            font=("Arial", 14),
            bg=self.COLORS["bg"],
            width=2
        )
        validation_label.pack(side="left", padx=5)
        
        # Label de error (centrado)
        error_label = tk.Label(
            frame,
            text="",
            font=("Arial", 8),
            bg=self.COLORS["bg"],
            fg=self.COLORS["error"],
            wraplength=300,
            justify="center"
        )
        error_label.pack()
        
        return entry, validation_label, error_label

    def validar_campo_nombre(self, nombre, validation_label, error_label):
        """Valida nombre en tiempo real"""
        if not nombre:
            validation_label.config(text="", fg=self.COLORS["bg"])
            error_label.config(text="")
            return False
        
        name_pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{1,25}$'
        if re.match(name_pattern, nombre):
            validation_label.config(text="✓", fg=self.COLORS["success"])
            error_label.config(text="")
            return True
        else:
            validation_label.config(text="✗", fg=self.COLORS["error"])
            error_label.config(text="Solo letras y espacios (máx 25 caracteres)")
            return False

    def validar_campo_email(self, email, validation_label, error_label):
        """Valida email en tiempo real"""
        if not email:
            validation_label.config(text="", fg=self.COLORS["bg"])
            error_label.config(text="")
            return False
        
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(email_pattern, email):
            validation_label.config(text="✓", fg=self.COLORS["success"])
            error_label.config(text="")
            return True
        else:
            validation_label.config(text="✗", fg=self.COLORS["error"])
            error_label.config(text="Formato de email inválido (ej: user@mail.com)")
            return False

    def validar_campo_password(self, password, validation_label, error_label):
        """Valida contraseña en tiempo real"""
        if not password:
            validation_label.config(text="", fg=self.COLORS["bg"])
            error_label.config(text="")
            return False
        
        errores = []
        if len(password) < 8:
            errores.append("mín. 8 caracteres")
        if not re.search(r'[A-Z]', password):
            errores.append("1 mayúscula")
        if not re.search(r'[0-9]', password):
            errores.append("1 número")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/]', password):
            errores.append("1 especial")
        
        if not errores:
            validation_label.config(text="✓", fg=self.COLORS["success"])
            error_label.config(text="")
            return True
        else:
            validation_label.config(text="✗", fg=self.COLORS["error"])
            error_label.config(text="Falta: " + ", ".join(errores))
            return False

    def vista_login(self):
        self.limpiar_pantalla()
        
        # Frame principal centrado
        main_frame = tk.Frame(self.container, bg=self.COLORS["bg"])
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        tk.Label(
            main_frame,
            text="🔑 Iniciar Sesión",
            font=("Segoe UI Emoji", 16, "bold"),
            bg=self.COLORS["bg"]
        ).pack(pady=20)
        
        # Campos con validación
        ent_email, val_email, err_email = self.crear_campo_validado(
            main_frame, "📧 Email:"
        )
        ent_pass, val_pass, err_pass = self.crear_campo_validado(
            main_frame, "🔒 Contraseña:", "*"
        )
        
        # Validación en tiempo real
        def on_email_change(*args):
            self.validar_campo_email(ent_email.get(), val_email, err_email)
        
        def on_pass_change(*args):
            password = ent_pass.get()
            if password:
                val_pass.config(text="🔒", fg=self.COLORS["text"])
                err_pass.config(text="")
        
        ent_email.bind('<KeyRelease>', on_email_change)
        ent_pass.bind('<KeyRelease>', on_pass_change)

        def ejecutar_login():
            email = ent_email.get().strip()
            password = ent_pass.get().strip()
            
            # Validar campos vacíos
            if not email:
                err_email.config(text="⚠️ El email es obligatorio")
                val_email.config(text="✗", fg=self.COLORS["error"])
                return
            
            if not password:
                err_pass.config(text="⚠️ La contraseña es obligatoria")
                val_pass.config(text="✗", fg=self.COLORS["error"])
                return
            
            # Validar formato de email
            if not self.validar_campo_email(email, val_email, err_email):
                messagebox.showerror("❌ Error", "El formato del email no es válido")
                return
            
            # Intentar login
            user = login(email, password)
            if user:
                self.usuario_actual = user
                messagebox.showinfo("✅ Éxito", f"¡Bienvenido, {user['name']}!")
                self.mostrar_menu_autenticado()
            else:
                messagebox.showerror(
                    "❌ Error de Acceso",
                    "Email o contraseña incorrectos.\nVerifica tus credenciales."
                )
                err_email.config(text="❌ Credenciales incorrectas")
                err_pass.config(text="❌ Credenciales incorrectas")
                val_email.config(text="✗", fg=self.COLORS["error"])
                val_pass.config(text="✗", fg=self.COLORS["error"])

        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.COLORS["bg"])
        btn_frame.pack(pady=20)
        
        self.crear_boton_icono(
            btn_frame,
            "🚀  Entrar",
            ejecutar_login,
            self.COLORS["primary"],
            width=28
        ).pack(pady=5)
        
        self.crear_boton_icono(
            btn_frame,
            "⬅️  Volver",
            self.mostrar_menu_invitado,
            "#757575",
            width=28
        ).pack(pady=5)

    def vista_registro(self):
        self.limpiar_pantalla()
        
        # Frame principal centrado
        main_frame = tk.Frame(self.container, bg=self.COLORS["bg"])
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        tk.Label(
            main_frame,
            text="✨ Crear Cuenta Nueva",
            font=("Segoe UI Emoji", 16, "bold"),
            bg=self.COLORS["bg"]
        ).pack(pady=20)
        
        # Campos con validación
        fields = {}
        
        ent_name, val_name, err_name = self.crear_campo_validado(
            main_frame, "👤 Nombre:"
        )
        fields["Nombre"] = (ent_name, val_name, err_name)
        
        ent_surname, val_surname, err_surname = self.crear_campo_validado(
            main_frame, "👥 Apellido:"
        )
        fields["Apellido"] = (ent_surname, val_surname, err_surname)
        
        ent_email, val_email, err_email = self.crear_campo_validado(
            main_frame, "📧 Email:"
        )
        fields["Email"] = (ent_email, val_email, err_email)
        
        ent_pass, val_pass, err_pass = self.crear_campo_validado(
            main_frame, "🔒 Contraseña:", "*"
        )
        fields["Contraseña"] = (ent_pass, val_pass, err_pass)
        
        # Validación en tiempo real
        def on_name_change(*args):
            self.validar_campo_nombre(ent_name.get(), val_name, err_name)
        
        def on_surname_change(*args):
            self.validar_campo_nombre(ent_surname.get(), val_surname, err_surname)
        
        def on_email_change(*args):
            self.validar_campo_email(ent_email.get(), val_email, err_email)
        
        def on_pass_change(*args):
            self.validar_campo_password(ent_pass.get(), val_pass, err_pass)
        
        ent_name.bind('<KeyRelease>', on_name_change)
        ent_surname.bind('<KeyRelease>', on_surname_change)
        ent_email.bind('<KeyRelease>', on_email_change)
        ent_pass.bind('<KeyRelease>', on_pass_change)

        def ejecutar_registro():
            nombre = ent_name.get().strip()
            apellido = ent_surname.get().strip()
            email = ent_email.get().strip()
            password = ent_pass.get().strip()
            
            # Validar todos los campos
            validaciones = [
                (nombre, val_name, err_name, "nombre", self.validar_campo_nombre),
                (apellido, val_surname, err_surname, "apellido", self.validar_campo_nombre),
                (email, val_email, err_email, "email", self.validar_campo_email),
                (password, val_pass, err_pass, "contraseña", self.validar_campo_password)
            ]
            
            errores = []
            for valor, val_label, err_label, campo, validador in validaciones:
                if not valor:
                    err_label.config(text=f"⚠️ El {campo} es obligatorio")
                    val_label.config(text="✗", fg=self.COLORS["error"])
                    errores.append(campo)
                elif not validador(valor, val_label, err_label):
                    errores.append(campo)
            
            if errores:
                messagebox.showerror(
                    "❌ Errores de Validación",
                    f"Corrige los siguientes campos:\n• " + "\n• ".join(errores)
                )
                return
            
            # Verificar si el usuario ya existe
            if userExists(email, password)[0]:
                messagebox.showwarning(
                    "⚠️ Usuario Existente",
                    "Ya existe una cuenta con este email"
                )
                err_email.config(text="❌ Este email ya está registrado")
                val_email.config(text="✗", fg=self.COLORS["error"])
                return
            
            # Crear usuario
            try:
                usuarios = cargar_usuarios()
                nuevo = createUser(nombre, apellido, email, password)
                usuarios.append(nuevo.to_dict())
                guardar_usuarios(usuarios)
                
                messagebox.showinfo(
                    "✅ Registro Exitoso",
                    f"¡Bienvenido, {nombre}!\nYa puedes iniciar sesión"
                )
                self.mostrar_menu_invitado()
            except Exception as e:
                messagebox.showerror("❌ Error", f"No se pudo crear el usuario: {e}")

        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.COLORS["bg"])
        btn_frame.pack(pady=20)
        
        self.crear_boton_icono(
            btn_frame,
            "✅  Registrar",
            ejecutar_registro,
            self.COLORS["secondary"],
            width=28
        ).pack(pady=5)
        
        self.crear_boton_icono(
            btn_frame,
            "⬅️  Volver",
            self.mostrar_menu_invitado,
            "#757575",
            width=28
        ).pack(pady=5)

    def mostrar_menu_autenticado(self):
        self.limpiar_pantalla()
        
        # Header con info del usuario
        header = tk.Frame(self.container, bg=self.COLORS["card"], relief=tk.RAISED, borderwidth=2)
        header.pack(pady=10, fill="x")
        
        tk.Label(
            header,
            text=f"👤 {self.usuario_actual['name']} {self.usuario_actual['surname']}",
            font=("Arial", 14, "bold"),
            bg=self.COLORS["card"]
        ).pack(pady=5)
        
        tk.Label(
            header,
            text=f"📧 {self.usuario_actual['email']}",
            font=("Arial", 9),
            bg=self.COLORS["card"],
            fg="#666666"
        ).pack(pady=2)
        
        # Título del panel
        tk.Label(
            self.container,
            text="⚡ Panel de Control",
            font=("Arial", 16, "bold"),
            bg=self.COLORS["bg"]
        ).pack(pady=15)

        # Frame centrado para botones
        btn_container = tk.Frame(self.container, bg=self.COLORS["bg"])
        btn_container.pack(expand=True)

        # Botones de funcionalidades con más ancho
        self.crear_boton_icono(
            btn_container,
            "📊  Ver Clasificación Megas",
            self.ver_clasificacion,
            "#607D8B",
            width=32
        ).pack(pady=8)

        self.crear_boton_icono(
            btn_container,
            "🌐  Web Scraping Pokémon Z-A",
            self.run_scraping_popup,
            "#9C27B0",
            width=32
        ).pack(pady=8)

        self.crear_boton_icono(
            btn_container,
            "⚔️  Consultar Mejores Movimientos",
            self.pedir_numero_pokedex,
            "#FF5722",
            width=32
        ).pack(pady=8)
        
        self.crear_boton_icono(
            btn_container,
            "🚪  Cerrar Sesión",
            self.logout,
            self.COLORS["danger"],
            width=32
        ).pack(pady=15)

    def ver_clasificacion(self):
        from src.scraping.ver_clasificacion import leer_clasificacion
        df = leer_clasificacion()
        if df is not None:
            mostrar_tabla_gui(df)

    def run_scraping_popup(self):
        popup = tk.Toplevel()
        popup.title("Scraping Pokémon Z-A")
        popup.geometry("450x200")
        popup.configure(bg=self.COLORS["bg"])
        
        tk.Label(
            popup,
            text="🌐 Web Scraping en Progreso",
            font=("Arial", 14, "bold"),
            bg=self.COLORS["bg"]
        ).pack(pady=20)
        
        status_label = tk.Label(
            popup,
            text="⏳ Iniciando...",
            font=("Arial", 11),
            bg=self.COLORS["bg"]
        )
        status_label.pack(pady=10)
        
        # Barra de progreso
        progress = ttk.Progressbar(popup, mode='indeterminate', length=300)
        progress.pack(pady=10)
        progress.start(10)

        def scraping_task():
            try:
                from src.scraping.scrape_pokemon_za import main as scrape_main
                status_label.config(text="📥 Descargando datos...")
                scrape_main()
                progress.stop()
                status_label.config(text="✅ ¡Scraping completado!")
                messagebox.showinfo("✅ Éxito", "Scraping completado correctamente")
            except Exception as e:
                progress.stop()
                messagebox.showerror("❌ Error", f"Ocurrió un error: {e}")
            finally:
                popup.destroy()

        Thread(target=scraping_task, daemon=True).start()

    def logout(self):
        respuesta = messagebox.askyesno(
            "🚪 Cerrar Sesión",
            "¿Estás seguro de que quieres cerrar sesión?"
        )
        if respuesta:
            self.usuario_actual = None
            messagebox.showinfo("👋", "¡Hasta pronto!")
            self.mostrar_menu_invitado()

    def pedir_numero_pokedex(self):
        """Abre un popup para introducir el número de Pokédex"""
        pokedex_number = simpledialog.askstring(
            "🔍 Buscar Pokémon",
            "Introduce el número de Pokédex:",
            parent=self.root
        )
        
        if pokedex_number:
            # Validar que sea un número
            if not pokedex_number.isdigit():
                messagebox.showerror("❌ Error", "Debes introducir un número válido")
                return
            
            Thread(target=self.scraping_movimientos, args=(pokedex_number,), daemon=True).start()

    def scraping_movimientos(self, pokedex_number):
        """Scraping de movimientos y muestra en ventana Treeview"""
        popup = tk.Toplevel(self.root)
        popup.title("Consultando movimientos...")
        popup.geometry("400x120")
        popup.configure(bg=self.COLORS["bg"])
        
        tk.Label(
            popup,
            text=f"🔍 Buscando Pokémon #{pokedex_number}...",
            font=("Arial", 12),
            bg=self.COLORS["bg"]
        ).pack(pady=20)
        
        progress = ttk.Progressbar(popup, mode='indeterminate', length=300)
        progress.pack(pady=10)
        progress.start(10)

        try:
            html = self.fetch_html(pokedex_number)
            soup = BeautifulSoup(html, "lxml")
            nombre = self.parse_pokemon_name(soup)
            movimientos = self.parse_movesets(soup)
            progress.stop()
            popup.destroy()
            
            if movimientos:
                self.mostrar_tabla_movimientos(nombre, pokedex_number, movimientos)
            else:
                messagebox.showwarning(
                    "⚠️ Sin Datos",
                    f"No se encontraron movimientos para el Pokémon #{pokedex_number}"
                )
        except Exception as e:
            progress.stop()
            popup.destroy()
            messagebox.showerror(
                "❌ Error",
                f"No se pudieron obtener los movimientos:\n{e}"
            )

    def fetch_html(self, pokedex_number):
        url = f"https://pokemon.gameinfo.io/en/pokemon/{pokedex_number}"
        headers = {"User-Agent": "Mozilla/5.0"}
        time.sleep(1)
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text

    def parse_pokemon_name(self, soup):
        title_tag = soup.find("h1")
        if title_tag:
            return title_tag.text.strip()
        return "Desconocido"

    def get_type_icon(self, type_name):
        """Obtiene el icono emoji para un tipo de Pokémon"""
        type_lower = type_name.lower()
        return self.TYPE_ICONS.get(type_lower, self.TYPE_ICONS["unknown"])
    
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
                        "Tipo": move_type,
                        "Icono": self.get_type_icon(move_type)
                    })
        return moves_data

    def mostrar_tabla_movimientos(self, nombre, pokedex_number, datos):
        ventana = tk.Toplevel(self.root)
        ventana.title(f"⚔️ Mejores Movimientos - {nombre} (#{pokedex_number})")
        ventana.geometry("750x450")
        ventana.configure(bg=self.COLORS["bg"])
        
        # Header
        header = tk.Frame(ventana, bg=self.COLORS["card"], relief=tk.RAISED, borderwidth=2)
        header.pack(pady=10, fill="x", padx=10)
        
        tk.Label(
            header,
            text=f"⚔️ {nombre.upper()}",
            font=("Arial", 16, "bold"),
            bg=self.COLORS["card"]
        ).pack(pady=5)
        
        tk.Label(
            header,
            text=f"Pokédex #{pokedex_number} • {len(datos)} movimientos encontrados",
            font=("Arial", 10),
            bg=self.COLORS["card"],
            fg="#666666"
        ).pack(pady=2)

        # Frame para la tabla
        frame = tk.Frame(ventana, bg=self.COLORS["bg"])
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Tabla con columna de icono
        tree = ttk.Treeview(
            frame,
            columns=["Categoría", "Movimiento", "Tipo", "Icono"],
            show="headings",
            height=15
        )
        
        tree.heading("Categoría", text="Categoría")
        tree.heading("Movimiento", text="Movimiento")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Icono", text="")
        
        tree.column("Categoría", width=120, anchor="center")
        tree.column("Movimiento", width=250, anchor="w")
        tree.column("Tipo", width=120, anchor="center")
        tree.column("Icono", width=50, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for mov in datos:
            tree.insert("", "end", values=[
                mov["Categoría"],
                mov["Movimiento"],
                mov["Tipo"],
                mov["Icono"]
            ])

        tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")


def mostrar_tabla_gui(df):
    if df is None or df.empty:
        messagebox.showwarning("⚠️ Sin datos", "No hay datos para mostrar.")
        return
    
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title("📊 Clasificación Megaevoluciones")
    ventana_tabla.geometry("900x550")
    
    # Header
    header = tk.Frame(ventana_tabla, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
    header.pack(pady=10, fill="x", padx=10)
    
    tk.Label(
        header,
        text="📊 CLASIFICACIÓN MEGAEVOLUCIONES",
        font=("Arial", 16, "bold"),
        bg="#ffffff"
    ).pack(pady=5)
    
    tk.Label(
        header,
        text=f"Total de registros: {len(df)}",
        font=("Arial", 10),
        bg="#ffffff",
        fg="#666666"
    ).pack(pady=2)

    frame = tk.Frame(ventana_tabla)
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

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