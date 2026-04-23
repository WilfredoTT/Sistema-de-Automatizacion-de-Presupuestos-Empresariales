import os
import sys
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AppInterface(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        base_path=os.path.dirname(__file__)
        ruta_icono=os.path.join(base_path, "..", "assets", "img", "IconoTd.ico")
        ruta_isotipotdn=os.path.join(base_path, "..", "assets", "img", "IsotipoTdN.png")
        
        if os.path.exists(ruta_icono):
            self.iconbitmap(ruta_icono)
        
        #Definición de estado inicial
        self.after(0, lambda: self.state('zoomed'))
        self.title("Sistema de Automatización de Presupuestos")
        
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
        
        try:
            self.isotipotdn_procesado=Image.open(ruta_isotipotdn)
            self.iconotdn=ctk.CTkImage(light_image=self.isotipotdn_procesado,
                                dark_image=self.isotipotdn_procesado,
                                size=(50,50))
        
            self.img_iconotdn = ctk.CTkLabel(self.menu_frame, image=self.iconotdn, text="")
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
        
        self.menu_frame.grid_rowconfigure(2, weight=1)
        
        self.btn_clssesion= ctk.CTkButton(self.menu_frame,
                                          text="CERRAR SESIÓN",
                                          fg_color=self.color_resalte,
                                          border_color=self.color_primario,
                                          border_width=2.5,
                                          width=150,
                                          height=35,
                                          font=("Arial", 14, "bold", "italic"),
                                          cursor="hand2",
                                          text_color=self.color_secundario,
                                          command=self.cerrar_sesion)
        self.btn_clssesion.grid(row=3, column=0, sticky="swe", pady=(0,5), padx=5)
        self.btn_clssesion.bind("<Enter>", self.al_entrar_mouse)
        self.btn_clssesion.bind("<Leave>", self.al_salir_mouse)
        
        #--ELEMENTOS DEL CONTENIDO--
        self.label_bienvenida = ctk.CTkLabel(
            self.main_frame, 
            text="Panel de Automatización de Presupuestos", 
            font=("Arial", 20, "bold"),
            text_color = self.color_resalte
        )
        self.label_bienvenida.grid(row=0, column=0, padx=10, pady=20, sticky="n")
    
    def cerrar_sesion(self):
        
        msg=CTkMessagebox(title="Sesion Cerrada",
                          message=f"¡Finalizada su Sesion con Éxito!",
                          option_1="Continuar",
                          icon="check")
        
        if msg.get() == "Continuar":
            self.destroy()#Cierra el dashboardPrincipal
        
    def al_entrar_mouse(self, event):
        self.btn_clssesion.configure(text="CERRAR SESION",
                                  text_color=self.color_secundario,
                                  fg_color=self.color_hverprincipal)
    
    def al_salir_mouse(self, event):
        self.btn_clssesion.configure(text_color=self.color_resalte,
                                  fg_color=self.color_secundario)    