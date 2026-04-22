import customtkinter as ctk
from database import validar_usuario
from tkinter import messagebox #Libreria para mensajes de alerta
from gui.app_interface import AppInterface
from PIL import Image
from CTkMessagebox import CTkMessagebox
import os
import sys

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #ASIGNACION DEL ICONO A LA VENTANA Y BARRA DE TAREAS
        ruta_icono=os.path.join(os.path.dirname(__file__), "..", "assets", "img", "IconoTd.ico")
        
        if os.path.exists(ruta_icono):
            self.iconbitmap(ruta_icono)
        
        #CREACIÓN DE VENTANA INICIAL
        self.title("Tedimeca.CA - Acceso al Sistema")
        self.after(0, lambda: self.state('zoomed'))
        ctk.set_appearance_mode("dark")
        
        #COLORES
        self.color_primario = "#E2C312"
        self.color_resalte = "#FFDE21"
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
        
        img_login=ctk.CTkImage(light_image=Image.open("assets/img/UsuarioLg.png"),
                               dark_image=Image.open("assets/img/UsuarioLg.png"),
                               size=(120,120))
        
        self.img_logo=ctk.CTkLabel(self.login_frame, image=img_login, text="")
        self.img_logo.grid(row=0, column=0, sticky="s")
        
        self.label_titulo = ctk.CTkLabel(self.login_frame, 
                                         text="Iniciar Sesión",
                                         font=("Arial", 28, "bold", "italic"),
                                         text_color=self.color_resalte,
                                         fg_color=self.color_secundario, 
                                         corner_radius=5,
                                         padx=5, pady=3)
        self.label_titulo.grid(row=1, column=0, pady=(0,15))
        
        self.user_entry = ctk.CTkEntry(self.login_frame, 
                                       placeholder_text="Usuario", 
                                       width=300, height=45,
                                       text_color=self.color_resalte,
                                       font=("Arial", 15, "bold"),
                                       justify="center",
                                       fg_color=self.color_secundario)
        self.user_entry.grid(row=2, column=0, pady=(0,5))

        self.pass_entry = ctk.CTkEntry(self.login_frame, 
                                       placeholder_text="Contraseña", 
                                       width=300, 
                                       height=45, 
                                       show="*",
                                       text_color=self.color_resalte,
                                       font=("Arial", 15, "bold"),
                                       justify="center",
                                       fg_color=self.color_secundario)
        self.pass_entry.grid(row=3, column=0, pady=(0,5))

        self.btn_entrar = ctk.CTkButton(self.login_frame, 
                                        text="ENTRAR", 
                                        fg_color=self.color_secundario, 
                                        text_color=self.color_resalte, 
                                        width=300, 
                                        height=45, 
                                        font=("Arial", 14, "bold"),
                                        cursor="hand2",
                                        command=self.validar_datos)
        self.btn_entrar.grid(row=4, column=0, pady=(10,0), sticky="n")
        self.btn_entrar.bind("<Enter>", self.al_entrar_mouse)
        self.btn_entrar.bind("<Leave>", self.al_salir_mouse)

        # --- LADO DERECHO: MARCA ---
        self.brand_frame = ctk.CTkFrame(self, fg_color=self.color_secundario, corner_radius=0)
        self.brand_frame.grid(row=0, column=1, sticky="nsew")
        self.brand_frame.grid_columnconfigure(0, weight=1)
        self.brand_frame.grid_rowconfigure((0, 3), weight=1)
        
        logo_img = ctk.CTkImage(light_image=Image.open("assets/img/LgTedimeca.png"),
                                dark_image=Image.open("assets/img/LgTedimeca.png"),
                                size=(400, 120))
            
        self.label_imagen = ctk.CTkLabel(self.brand_frame, image=logo_img, text="")
        self.label_imagen.grid(row=1, column=0, pady=(0,1))

        self.label_logo = ctk.CTkLabel(self.brand_frame, 
                                       text="TEDIMECA.CA", 
                                       font=("Arial", 65, "bold", "italic"), 
                                       text_color=self.color_resalte)
        self.label_logo.grid(row=2, column=0, pady=(0, 20))
        
        self.label_slogan = ctk.CTkLabel(self.brand_frame, 
                                         text="Soluciones Industriales de Precisión", 
                                         font=("Arial", 25), 
                                         text_color=self.color_resalte)
        self.label_slogan.grid(row=2, column=0, pady=(70, 0))
    
    def al_entrar_mouse(self, event):
        self.btn_entrar.configure(text="¿LISTO PARA TRABAJAR?",
                                  text_color=self.color_secundario,
                                  fg_color=self.color_hverprincipal)
    
    def al_salir_mouse(self, event):
        self.btn_entrar.configure(text="ENTRAR",
                                  text_color=self.color_resalte,
                                  fg_color=self.color_secundario)
        
    #Validación de datos
    def validar_datos(self):
        usuario = self.user_entry.get()
        contrasena = self.pass_entry.get()
    
        resultado = validar_usuario(usuario, contrasena)
        
        
        if resultado:
            rol = resultado[0] #almacenamiento de rol por si se debe utilizar
            print(f"¡Acceso concedido como {rol}!")#alerta sistema
            
            #Alerta pantalla
            msg= CTkMessagebox(title="Acceso Concedido", 
                               message=f"¡Acceso concedido como {rol}!", 
                               option_1="Continuar", 
                               icon="check")
            
            if msg.get() == "Continuar":
                self.destroy()#Cierre de login
            
            #apertura interfaz principal
            app_interface = AppInterface()
            app_interface.mainloop()
        else:
            msg= CTkMessagebox(title="Acceso Denegado", 
                               message="Credenciales incorrectas", 
                               option_1="Intentar de Nuevo", 
                               icon="cancel")
            
            if msg.get() == "Intentar de Nuevo":
                self.user_entry.delete(0, "end")
                self.pass_entry.delete(0, "end")
               