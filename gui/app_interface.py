import os
import sys
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
from PIL import Image
from CTkTable import *
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import registrar_usuario, obtener_usuarios, anular_usuario_db, actualizar_usuario_db, desanular_usuario_db

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class AppInterface(ctk.CTkToplevel):
    def __init__(self, user_data):
        super().__init__()
        
        #GUARDAR INFORMACIÓN DE SESIÓN
        self.user_id = user_data[0]
        self.username = user_data[1]
        self.rol = user_data[2]
        
        base_path = Path(__file__).resolve().parent
        root_path = base_path.parent
        ruta_icono = root_path / "assets" / "img" / "IconoTd.ico"
        ruta_isotipotdn = root_path / "assets"/ "img"/ "IsotipoTdN.png"
        
        if os.path.exists(ruta_icono):
            try:
                self.after(200, lambda: self.iconbitmap(ruta_icono))
            except:
                pass
        
        #Definición de estado inicial
        self.after(0, lambda: self.state('zoomed'))
        self.title(f"Sistema de Automatización de Presupuestos - PresuQuest - Tedimeca.Ca - DashboardPrincipal - {self.username} - ({self.rol})")
        
        #Configuración de la Red(Su esqueleto)
        self.grid_columnconfigure(0, weight=0) #Menú fijo
        self.grid_columnconfigure(1, weight=1) #Columna de trabajo expansible
        self.grid_rowconfigure(0, weight=1)
        
        #Creación de contenedores
        #Frame del menú natural
        self.menu_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew") #NSEW Se pega a las 4 paredes
        
        #COLORES
        self.color_primario = "#E2C312"
        self.color_resalte = "#FFDE21"
        self.color_hverprincipal = "#AD950C"
        self.color_secundario = "#222222"
        
        #Frame de Contenido Principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.columnconfigure(0, weight=1)
        
        #--ELEMENTOS DEL MENÚ--
        self.dibujar_elementos_menu(ruta_isotipotdn=ruta_isotipotdn)
        self.crear_botones_dinamicos()
        
        self.menu_frame.grid_rowconfigure(15, weight=1)
        
        self.btn_clssesion= ctk.CTkButton(self.menu_frame,
                                          text="CERRAR SESIÓN",
                                          fg_color=self.color_secundario,
                                          border_color=self.color_primario,
                                          border_width=2.5,
                                          width=150,
                                          height=35,
                                          font=("Arial", 14, "bold", "italic"),
                                          cursor="hand2",
                                          text_color=self.color_primario,
                                          command=self.cerrar_sesion)
        self.btn_clssesion.grid(row=16, column=0, sticky="swe", pady=(0,5), padx=5)
        self.btn_clssesion.bind("<Enter>", lambda event: self.al_entrar_mouse(event, self.btn_clssesion))
        self.btn_clssesion.bind("<Leave>", lambda event: self.al_salir_mouse(event, self.btn_clssesion))
        
        #--ELEMENTOS DEL CONTENIDO--
        self.label_bienvenida = ctk.CTkLabel(
            self.main_frame, 
            text="Panel de Automatización de Presupuestos", 
            font=("Arial", 20, "bold"),
            text_color = self.color_resalte
        )
        self.label_bienvenida.grid(row=0, column=0, padx=10, pady=20, sticky="n")
        
        self.protocol("WM_DELETE_WINDOW" , lambda: (self.destroy(), self.quit()))
        
    def dibujar_elementos_menu(self, ruta_isotipotdn):
        try:
            self.isotipotdn_procesado=Image.open(ruta_isotipotdn)
            self.iconotdn=ctk.CTkImage(light_image=self.isotipotdn_procesado,
                                dark_image=self.isotipotdn_procesado,
                                size=(50,50))
        
            self.img_iconotdn = ctk.CTkLabel(master=self.menu_frame, image=self.iconotdn, text="")
            self.img_iconotdn.image=self.iconotdn
            self.img_iconotdn.grid(row=0, column=0, sticky="s", pady=(20,0))
        
        except Exception as e:
            print(f"ERROR AL CARGAR LA IMAGEN {e}")
            self.img_iconotdn = ctk.CTkLabel(self.menu_frame, text="[INSERTE IMAGEN AQUI]", text_color=self.color_resalte)
            self.img_iconotdn.grid(row=0, column=0, sticky="s", pady=(20,0))
        
        self.label_empresa = ctk.CTkLabel(
            self.menu_frame,
            text = "Tedimeca.CA",
            font = ("Arial", 24, "bold"),
            text_color = self.color_resalte
        )
        self.label_empresa.grid(row=1, column=0, padx=30, pady=(0,20), sticky="n")
        
    def crear_botones_dinamicos(self):
        row_cont = 2
        
        # 1. SECCIÓN DE ADMINISTRACIÓN (Solo Maestro - AHORA ARRIBA)
        if self.rol == "Maestro":
            # Fila 2
            self.lbl_admin_title = ctk.CTkLabel(self.menu_frame, text="ADMINISTRACIÓN", 
                                               font=("Arial", 11, "bold"), text_color=self.color_resalte)
            self.lbl_admin_title.grid(row=row_cont, column=0, pady=(10, 5))
            row_cont += 1 # Fila 3
            
            self.btn_ctrusuarios = ctk.CTkButton(self.menu_frame, text="👤⚙️ Control de Usuarios",
                                             fg_color=self.color_secundario, anchor="center",
                                             text_color=self.color_primario, border_color=self.color_primario,
                                             border_width= 1.5, height=25, font=("Arial", 14, "italic"),
                                             cursor="hand2", command=self.mostrar_tabla_pro)
            self.btn_ctrusuarios.grid(row=row_cont, column=0, padx=10, pady=5, sticky="ew")
            self.btn_ctrusuarios.bind("<Enter>", lambda event: self.al_entrar_mouse(event, self.btn_ctrusuarios))
            self.btn_ctrusuarios.bind("<Leave>", lambda event: self.al_salir_mouse(event, self.btn_ctrusuarios))
            row_cont += 1 # Fila 4
            
            self.btn_personal = ctk.CTkButton(self.menu_frame, text="👥 Ficha de Personal", 
                                             fg_color=self.color_secundario, anchor="center",
                                             text_color=self.color_primario, border_color=self.color_primario,
                                             border_width= 1.5, height=25, font=("Arial", 14, "italic"),
                                             cursor="hand2", command=self.mostrar_modulo_maestro)
            self.btn_personal.grid(row=row_cont, column=0, padx=10, pady=5, sticky="ew")
            self.btn_personal.bind("<Enter>", lambda event: self.al_entrar_mouse(event, self.btn_personal))
            self.btn_personal.bind("<Leave>", lambda event: self.al_salir_mouse(event, self.btn_personal))
            row_cont += 1 # Fila 5
            
            self.btn_logs = ctk.CTkButton(self.menu_frame, text="📜 Auditoría (Logs)", 
                                         fg_color=self.color_secundario, anchor="center",
                                         text_color=self.color_primario, border_color=self.color_primario,
                                         border_width= 1.5, height=25, font=("Arial", 14, "italic"),
                                         cursor="hand2", command=lambda: print("Logs"))
            self.btn_logs.grid(row=row_cont, column=0, padx=10, pady=5, sticky="ew")
            self.btn_logs.bind("<Enter>", lambda event: self.al_entrar_mouse(event, self.btn_logs))
            self.btn_logs.bind("<Leave>", lambda event: self.al_salir_mouse(event, self.btn_logs))
            row_cont += 1 # Fila 6
            
            self.btn_asistencia = ctk.CTkButton(self.menu_frame, text="📅 Asistencia Trabajadores",
                                                fg_color=self.color_secundario, anchor="center",
                                                text_color=self.color_primario, border_color=self.color_primario,
                                                border_width= 1.5, height=25, font=("Arial", 14, "italic"),
                                                cursor="hand2", command=lambda:print("ASISTENCIAS"))
            self.btn_asistencia.grid(row=row_cont, column=0, padx=10, pady=5, sticky="ew")
            self.btn_asistencia.bind("<Enter>", lambda event: self.al_entrar_mouse(event, self.btn_asistencia))
            self.btn_asistencia.bind("<Leave>", lambda event: self.al_salir_mouse(event, self.btn_asistencia))
            row_cont += 1 #Fila 7

            # Un separador visual para diferenciar de lo operativo
            ctk.CTkLabel(self.menu_frame, text="OPERACIONES", 
                         font=("Arial", 11, "bold"), text_color=self.color_resalte).grid(row=row_cont, column=0, pady=(15, 5))
            row_cont += 1 # Fila 8

        # 2. BOTONES OPERATIVOS (Para todos)
        self.btn_dash = ctk.CTkButton(self.menu_frame, text="📊 Dashboard", 
                                     fg_color=self.color_secundario, anchor="center",
                                     text_color=self.color_primario, border_color=self.color_primario,
                                     border_width= 1.5, height=25, font=("Arial", 14, "italic"),
                                     cursor="hand2", command=lambda: print("Dash"))
        self.btn_dash.grid(row=row_cont, column=0, padx=10, pady=5, sticky="ew")
        self.btn_dash.bind("<Enter>", lambda event: self.al_entrar_mouse(event, self.btn_dash))
        self.btn_dash.bind("<Leave>", lambda event: self.al_salir_mouse(event, self.btn_dash))
        row_cont += 1 # Fila 9

        self.btn_presu = ctk.CTkButton(self.menu_frame, text="📝 Presupuestos", 
                                      fg_color=self.color_secundario, anchor="center",
                                      text_color=self.color_primario, border_color=self.color_primario,
                                      border_width= 1.5, height=25, font=("Arial", 14, "italic"),
                                      cursor="hand2", command=lambda: print("Presu"))
        self.btn_presu.grid(row=row_cont, column=0, padx=10, pady=5, sticky="ew")
        self.btn_presu.bind("<Enter>", lambda event: self.al_entrar_mouse(event, self.btn_presu))
        self.btn_presu.bind("<Leave>", lambda event: self.al_salir_mouse(event, self.btn_presu))
        
        row_cont += 1 # Fila 10
            
        self.lbl_admin_title = ctk.CTkLabel(self.menu_frame, text="INVENTARIO", 
                                               font=("Arial", 11, "bold"), text_color=self.color_resalte)
        self.lbl_admin_title.grid(row=row_cont, column=0, pady=(10, 5))
        row_cont += 1 # Fila 11
            
        self.btn_inventario = ctk.CTkButton(self.menu_frame, text="📦 Inventario", 
                                    fg_color=self.color_secundario, anchor="center",
                                    text_color=self.color_primario, border_color=self.color_primario,
                                    border_width= 1.5, height=25, font=("Arial", 14, "italic"),
                                    cursor="hand2", command=lambda: print("Inventario"))
        self.btn_inventario.grid(row=row_cont, column=0, padx=10, pady=5, sticky="ew")
        self.btn_inventario.bind("<Enter>", lambda event: self.al_entrar_mouse(event, self.btn_inventario))
        self.btn_inventario.bind("<Leave>", lambda event: self.al_salir_mouse(event, self.btn_inventario))

    def mostrar_modulo_maestro(self):
        # Aquí limpiarás el main_frame y cargarás la clase que hicimos antes
        print("Cargando módulo maestro...")
    
    def cerrar_sesion(self):
        
        msg=CTkMessagebox(title="Finalizar Sesion",
                          message=f"¿Desea cerrar su sesión?",
                          option_1="Si",
                          option_2="No",
                          icon="check")
        
        if msg.get() == "Si":
            self.destroy()#Cierra el dashboardPrincipal
        
    def al_entrar_mouse(self, event, boton):
        boton.configure(text_color=self.color_secundario,
                                  fg_color=self.color_hverprincipal)
    
    def al_salir_mouse(self, event, boton):
        boton.configure(text_color=self.color_resalte,
                                  fg_color=self.color_secundario)
    
    def crear_menu_lateral(self, rol_usuario):
    # Botones comunes para todos
        self.btn_dash = ctk.CTkButton(self.sidebar, text="Dashboard", command=self.mostrar_dash)
        self.btn_dash.pack(pady=10)
        
        self.btn_presupuestos = ctk.CTkButton(self.sidebar, text="Presupuestos", command=self.mostrar_presu)
        self.btn_presupuestos.pack(pady=10)
            
    def limpiar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
    def mostrar_tabla_pro(self):
        self.fila_seleccionada_idx = None # Resetear selección al recargar tabla
        self.limpiar_main_frame()
        
        # 1. TÍTULO (Fila 0)
        lbl_titulo = ctk.CTkLabel(self.main_frame, text="Gestión de Usuarios", 
                                 font=("Arial", 25, "bold"), text_color=self.color_resalte)
        lbl_titulo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # 2. CONTENEDOR DE CABECERA (Fila 1: Botones + Buscador)
        # Usamos un solo frame para que todo esté en la misma línea
        self.frame_acciones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_acciones.grid(row=1, column=0, padx=20, pady=10, sticky="ew") 

        # Configuración de columnas del frame de acciones
        # La columna 4 será el "resorte" que empuja el buscador a la derecha
        self.frame_acciones.grid_columnconfigure(4, weight=1)
        
        # Botones de Acción (Columnas 0 a 3)
        btn_add = ctk.CTkButton(self.frame_acciones, text="+ Agregar", width=100,
                               fg_color=self.color_secundario, border_color=self.color_primario,
                               border_width=1, text_color=self.color_resalte, command=self.abrir_formulario_usuario, cursor="hand2")
        btn_add.grid(row=0, column=0, padx=5)
        btn_add.bind("<Enter>", lambda event: self.al_entrar_mouse(event, btn_add))
        btn_add.bind("<Leave>", lambda event: self.al_salir_mouse(event, btn_add))

        btn_edit = ctk.CTkButton(self.frame_acciones, text="✏️ Editar", width=100,
                                fg_color=self.color_secundario, border_color=self.color_primario,
                                border_width=1, text_color=self.color_resalte, command=self.preparar_edicion, cursor="hand2")
        btn_edit.grid(row=0, column=1, padx=5)

        btn_del = ctk.CTkButton(self.frame_acciones, text="🚫 Anular", width=100,
                               fg_color="#A34343", hover_color="#823232", command=self.ejecutar_anulacion, cursor="hand2")
        btn_del.grid(row=0, column=2, padx=5)
        
        btn_desanular = ctk.CTkButton(self.frame_acciones, text="Desanular", 
                             command=self.preparar_desanulacion,
                             fg_color="#27ae60", hover_color="#2ecc71", width=120, cursor="hand2")
        btn_desanular.grid(row=0, column=3, padx=5)

        # 3. BUSCADOR (Ubicado en la columna 5 del frame de acciones)
        self.entry_buscar = ctk.CTkEntry(
            self.frame_acciones, 
            placeholder_text="🔍 Buscar por nombre o rol...",
            width=350,
            height=35,
            border_color=self.color_primario,
            text_color=self.color_resalte,
            border_width=1.5)
        # sticky="e" lo pega a la derecha de la pantalla
        self.entry_buscar.grid(row=0, column=5, padx=5, sticky="e")
        self.entry_buscar.bind("<KeyRelease>", self.filtrar_usuarios_evento)

        # 4. DATOS Y TABLA (Fila 2 del main_frame)
        header = [["ID", "Usuario", "Rol", "Estado"]]
        cuerpo = obtener_usuarios() 
        value = header + cuerpo

        self.table = CTkTable(master=self.main_frame, 
                              column=4, 
                              row=len(value), 
                              values=value,
                              colors=["#2a2a2a", "#212121"],
                              header_color=self.color_secundario,
                              hover_color="#333333",
                              text_color=self.color_resalte,
                              command=self.seleccionar_fila_evento)
        
        # IMPORTANTE: sticky="nsew" para que la tabla se estire
        self.table.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        self.table.bind("<Enter>", lambda e: e.widget.configure(cursor="hand2"))
        self.table.bind("<Leave>", lambda e: e.widget.configure(cursor="arrow"))

        # 5. CONFIGURACIÓN FINAL DE EXPANSIÓN
        # Esto hace que la columna 0 y la fila 2 del main_frame ocupen todo el espacio disponible
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
    
    def abrir_formulario_usuario(self, edit_data=None):
        ventana_add = ctk.CTkToplevel(self)
        titulo_ventana = "Editar Usuario" if edit_data else "Registro de Usuario"
        ventana_add.title(f"{titulo_ventana} - Tedimeca.CA")
        ventana_add.after(0, lambda: ventana_add.state('zoomed'))
        base_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.abspath(os.path.join(base_path, ".."))
        ruta_icono = os.path.join(root_path, "assets", "img", "IconoTd.ico")
        
        def establecer_icono():
            # Verificamos que la ventana siga viva antes de aplicar el icono
            if ventana_add.winfo_exists():
                try:
                    ventana_add.iconbitmap(ruta_icono)
                except:
                    pass

        if os.path.exists(ruta_icono):
            # Usamos una función que verifique la existencia
            ventana_add.after(200, establecer_icono)

        ventana_add.grab_set()
        
        frame_central = ctk.CTkFrame(ventana_add, fg_color="transparent")
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(frame_central, text=titulo_ventana, 
                     font=("Arial", 30, "bold"), # Fuente más grande para el modo zoomed
                     text_color=self.color_resalte).pack(pady=(0, 30))

        entry_nom = ctk.CTkEntry(frame_central, placeholder_text="Nombre de Usuario", 
                                 width=350, height=45, font=("Arial", 14))
        entry_nom.pack(pady=10)

        entry_pass = ctk.CTkEntry(frame_central, placeholder_text="Contraseña (Nueva si edita)", 
                                  show="*", width=350, height=45, font=("Arial", 14))
        entry_pass.pack(pady=10)

        combo_rol = ctk.CTkComboBox(frame_central, values=["Maestro", "Administrador", "Supervisor"], 
                                    width=350, height=45, font=("Arial", 14))
        combo_rol.pack(pady=10)

        if edit_data:
            entry_nom.insert(0, edit_data[1])
            combo_rol.set(edit_data[2])

        def guardar():
            u, p, r = entry_nom.get(), entry_pass.get(), combo_rol.get()
            
            if u.strip() == "":
                CTkMessagebox(title="Error", message="El nombre es obligatorio", icon="cancel")
                return

            if edit_data:
                exito, mensaje = actualizar_usuario_db(edit_data[0], u, p, r)
                if exito:
                    self.focus_set()
                    CTkMessagebox(title="Éxito", message=mensaje, icon="check")
                    self.mostrar_tabla_pro()
                    ventana_add.after(50, ventana_add.destroy)
                else:
                    CTkMessagebox(title="Error", message=mensaje, icon="cancel")
            else:
                if p.strip() == "":
                    CTkMessagebox(title="Error", message="La contraseña es obligatoria", icon="cancel")
                    return
                
                exito, mensaje = registrar_usuario(u, p, r)
                if exito:
                    self.focus_set()
                    CTkMessagebox(title="Éxito", message=mensaje, icon="check")
                    self.mostrar_tabla_pro()
                    ventana_add.after(50, ventana_add.destroy)
                else:
                    CTkMessagebox(title="Error", message=mensaje, icon="cancel")

        btn_guardar = ctk.CTkButton(frame_central, text="GUARDAR CAMBIOS", 
                                    command=guardar, width=350, height=50,
                                    font=("Arial", 16, "bold"), cursor="hand2",
                                    fg_color=self.color_secundario,
                                    border_color=self.color_primario,
                                    border_width=2,
                                    text_color=self.color_primario)
        btn_guardar.pack(pady=40)
        
        # Efecto hover para el botón de guardar
        btn_guardar.bind("<Enter>", lambda e: btn_guardar.configure(fg_color=self.color_hverprincipal, text_color=self.color_secundario))
        btn_guardar.bind("<Leave>", lambda e: btn_guardar.configure(fg_color=self.color_secundario, text_color=self.color_primario))
    
    def ejecutar_anulacion(self):
        usuario = self.obtener_seleccion_tabla()
        if usuario:
            # usuario[0] es el ID, usuario[1] es el nombre
            pregunta = CTkMessagebox(title="Confirmar", 
                                     message=f"¿Seguro que desea anular a {usuario[1]}?",
                                     icon="question", option_1="Sí", option_2="No")
            
            if pregunta.get() == "Sí":
                # Llamada a database.py
                exito, mensaje = anular_usuario_db(usuario[0])
                if exito:
                    CTkMessagebox(title="Éxito", message=mensaje, icon="check")
                    self.mostrar_tabla_pro() # Recargar tabla
                else:
                    CTkMessagebox(title="Error", message=mensaje, icon="cancel")
                    
    def preparar_edicion(self):
        usuario = self.obtener_seleccion_tabla()
        if usuario:
            # Abrimos el mismo formulario pero le pasamos los datos para "Editar"
            self.abrir_formulario_usuario(edit_data=usuario)
            
    def preparar_desanulacion(self):
        # Verificamos si hay una fila seleccionada
        idx = getattr(self, "fila_seleccionada_idx", None)
        
        if idx is None:
            CTkMessagebox(title="Atención", message="Por favor, seleccione un usuario de la tabla", icon="warning")
            return

        # Obtenemos los datos de la fila (el ID está en la columna 0)
        datos_fila = self.table.get_row(idx)
        id_usuario = datos_fila[0]
        nombre_usuario = datos_fila[1]
        estado_actual = datos_fila[3] # La columna nueva de 'Estatus'

        if estado_actual == "Activo":
            CTkMessagebox(title="Información", message="Este usuario ya se encuentra Activo", icon="info")
            return

        # Preguntamos antes de proceder
        confirmar = CTkMessagebox(title="Confirmar", 
                                message=f"¿Desea restaurar el acceso para {nombre_usuario}?",
                                icon="question", option_1="Si", option_2="No")
        
        if confirmar.get() == "Sí":
            exito, mensaje = desanular_usuario_db(id_usuario)
            if exito:
                CTkMessagebox(title="Éxito", message=mensaje, icon="check")
                self.mostrar_tabla_pro() # Refrescamos para ver el cambio de 'Anulado' a 'Activo'
            else:
                CTkMessagebox(title="Error", message=mensaje, icon="cancel")
            
    def seleccionar_fila_evento(self, data):
        row = data["row"]
        
        # Ignorar clics en el encabezado (Fila 0)
        if row == 0: return 

        # 1. Limpieza: Resetear todas las filas al color original (alternado)
        for i in range(1, self.table.rows):
            # Usamos los colores alternos que definiste originalmente
            color_base = "#2a2a2a" if i % 2 == 0 else "#212121"
            self.table.edit_row(i, fg_color=color_base, text_color=self.color_resalte)
        
        # 2. Resalte: Aplicar color de énfasis a la fila seleccionada
        self.table.edit_row(row, fg_color=self.color_hverprincipal, text_color=self.color_secundario)
        
        # 3. Persistencia: Guardar el índice para operaciones posteriores
        self.fila_seleccionada_idx = row
        
    def obtener_seleccion_tabla(self):
        # Verificamos si existe el atributo y si es válido
        idx = getattr(self, "fila_seleccionada_idx", None)
        
        # Validar que se haya seleccionado una fila válida (mayor a 0)
        if idx is not None and idx > 0:
            try:
                # Retorna una lista con [ID, Usuario, Rol, Estado]
                datos_fila = self.table.get_row(idx)
                return datos_fila
            except Exception as e:
                print(f"Error al recuperar datos: {e}")
                return None
        else:
            # Notificación formal al usuario en caso de omisión
            CTkMessagebox(title="Aviso", 
                          message="Por favor, haga clic sobre un usuario en la tabla para seleccionarlo.", 
                          icon="warning")
            return None
        
    def filtrar_usuarios_evento(self, event=None):
        """Filtra la lista de usuarios en tiempo real según la entrada del buscador."""
        busqueda = self.entry_buscar.get().lower()
        
        # Recuperar datos frescos de la base de datos
        cuerpo_completo = obtener_usuarios() 
        
        # Filtrar filas: buscamos coincidencia en Usuario (índice 1) o Rol (índice 2)
        cuerpo_filtrado = [
            fila for fila in cuerpo_completo 
            if busqueda in fila[1].lower() or busqueda in fila[2].lower()
        ]
        
        # Actualizar la tabla con los nuevos valores (incluyendo cabecera)
        header = [["ID", "Usuario", "Rol", "Estado"]]
        self.table.update_values(header + cuerpo_filtrado)
        
        #Limpiar la selección visual al filtrar
        self.fila_seleccionada_idx = None
        