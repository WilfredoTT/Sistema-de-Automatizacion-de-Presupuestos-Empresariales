import customtkinter as ctk
from database import validar_usuario
from tkinter import messagebox #Libreria para mensajes de alerta
from gui.app_interface import AppInterface

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #CREACIÓN DE VENTANA INICIAL
        self.title("Tedimeca.CA - Acceso al Sistema")
        self.after(0, lambda: self.state('zoomed'))
        ctk.set_appearance_mode("dark")
        
        #COLORES
        self.color_primario = "#FFDE21"
        self.color_hverprincipal = "#AD950C"
        self.color_secundario = "#222222"
        
        #CREACIÓN Y CONFIGURACIÓN DEL GRID PRINCIPAL (2 COLUMNAS)
        self.grid_columnconfigure(0, weight=1)#COLUMNA LOGIN
        self.grid_columnconfigure(1, weight=1)#COLUMNA LOGO/MARCA
        self.grid_rowconfigure(0, weight=1)
        
        #---LADO IZQUIERDO: FORMULARIO---
        self.login_frame = ctk.CTkFrame(self, fg_color=self.color_primario)
        self.login_frame.grid(row = 0, column = 0, sticky = "nsew")
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure((0,4), weight=1) #ESPACIOS ELÁSTICOS
        
        self.label_titulo = ctk.CTkLabel(self.login_frame, 
                                         text="Iniciar Sesión",
                                         font=("Arial", 28, "bold", "italic"),
                                         text_color=self.color_primario,
                                         fg_color=self.color_secundario, 
                                         corner_radius=5,
                                         padx=5, pady=3)
        self.label_titulo.grid(row=1, column=0, pady=(0,20))
        
        self.user_entry = ctk.CTkEntry(self.login_frame, 
                                       placeholder_text="Usuario", 
                                       width=300, height=45,
                                       text_color="white",
                                       fg_color=self.color_secundario)
        self.user_entry.grid(row=2, column=0, pady=10)

        self.pass_entry = ctk.CTkEntry(self.login_frame, 
                                       placeholder_text="Contraseña", 
                                       width=300, 
                                       height=45, 
                                       show="*",
                                       text_color="white",
                                       fg_color=self.color_secundario)
        self.pass_entry.grid(row=3, column=0, pady=10)

        self.btn_entrar = ctk.CTkButton(self.login_frame, 
                                        text="ENTRAR", 
                                        fg_color=self.color_secundario, 
                                        text_color=self.color_primario, 
                                        width=300, 
                                        height=45, 
                                        font=("Arial", 14, "bold"),
                                        cursor="hand2",
                                        command=self.validar_datos)
        self.btn_entrar.grid(row=4, column=0, pady=20, sticky="n")
        self.btn_entrar.bind("<Enter>", self.al_entrar_mouse)
        self.btn_entrar.bind("<Leave>", self.al_salir_mouse)

        # --- LADO DERECHO: MARCA ---
        self.brand_frame = ctk.CTkFrame(self, fg_color=self.color_secundario, corner_radius=0)
        self.brand_frame.grid(row=0, column=1, sticky="nsew")
        self.brand_frame.grid_columnconfigure(0, weight=1)
        self.brand_frame.grid_rowconfigure((0, 2), weight=1)

        self.label_logo = ctk.CTkLabel(self.brand_frame, 
                                       text="TEDIMECA.CA", 
                                       font=("Arial", 50, "bold", "italic"), 
                                       text_color=self.color_primario)
        self.label_logo.grid(row=1, column=0)
        
        self.label_slogan = ctk.CTkLabel(self.brand_frame, 
                                         text="Soluciones Industriales de Precisión", 
                                         font=("Arial", 18), 
                                         text_color=self.color_primario)
        self.label_slogan.grid(row=1, column=0, pady=(80, 0))
    
    def al_entrar_mouse(self, event):
        self.btn_entrar.configure(text="¿LISTO PARA TRABAJAR?",
                                  text_color=self.color_secundario,
                                  fg_color=self.color_hverprincipal)
    
    def al_salir_mouse(self, event):
        self.btn_entrar.configure(text="ENTRAR",
                                  text_color=self.color_primario,
                                  fg_color=self.color_secundario)
        
    #Validación de datos
    def validar_datos(self):
        usuario = self.user_entry.get()
        contrasena = self.pass_entry.get()
        
        resultado = validar_usuario(usuario, contrasena)
        
        if resultado:
            rol = resultado[0] #almacenamiento de rol por si se debe utilizar
            print(f"¡Acceso concedido como {rol}!")
            
            #cerrar ventana de login
            self.destroy()
            
            #apertura interfaz principal
            app_interface = AppInterface()
            app_interface.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
               