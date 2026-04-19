import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #Definición de estado inicial
        self.after(0, lambda: self.state('zoomed'))
        self.title("Sistema de Automatización de Presupuestos")
        
        #Configuración de la Red(Su esqueleto)
        self.grid_columnconfigure(0, weight=0) #Menú fijo
        self.grid_columnconfigure(1, weight=1) #Columna de trabajo expansible
        self.grid_rowconfigure(0, weight=1)
        
        #Creación de contenedores
        #Frame del menú natural
        self.menu_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew") #NSEW Se pega a las 4 paredes  
        
        #Frame de Contenido Principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
app = App()
app.mainloop()