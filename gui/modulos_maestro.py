import customtkinter as ctk
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox
import uuid
from database import obtener_usuarios

class ModuloMaestro(ctk.CTkFrame):
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, **kwargs)
        
        self.app = app_instance # Guardamos la referencia a AppInterface
        
        # Configuración de cuadrícula (Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crear Tabview (Pestañas)
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#1f538d")
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Añadir pestañas
        self.tab_trabajadores = self.tabview.add("Gestión de Trabajadores")
        self.tab_usuarios = self.tabview.add("Accesos al Sistema")

        self.setup_tab_trabajadores()
        self.setup_tab_usuarios()

    def setup_tab_trabajadores(self):
        # --- Formulario Lateral (Izquierda) ---
        self.frame_form = ctk.CTkFrame(self.tab_trabajadores, width=300)
        self.frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.frame_form, text="Ficha del Trabajador", font=("Arial", 16, "bold")).pack(pady=10)

        self.entry_cedula = ctk.CTkEntry(self.frame_form, placeholder_text="Cédula (V-00000000)")
        self.entry_cedula.pack(fill="x", padx=10, pady=5)

        self.entry_nombre = ctk.CTkEntry(self.frame_form, placeholder_text="Nombre Completo")
        self.entry_nombre.pack(fill="x", padx=10, pady=5)

        self.combo_cargo = ctk.CTkComboBox(self.frame_form, values=["Ayudante_General", "Mecanico", "Supervisor"])
        self.combo_cargo.pack(fill="x", padx=10, pady=5)
        self.combo_cargo.set("Ayudante_General")

        self.entry_salario_lv = ctk.CTkEntry(self.frame_form, placeholder_text="Salario L-V (USD)")
        self.entry_salario_lv.pack(fill="x", padx=10, pady=5)

        self.btn_guardar = ctk.CTkButton(self.frame_form, text="Registrar Personal", 
                                        fg_color="#2ecc71", hover_color="#27ae60",
                                        command=self.guardar_trabajador)
        self.btn_guardar.pack(fill="x", padx=10, pady=20)

        # --- Tabla de Visualización (Derecha) ---
        self.frame_tabla = ctk.CTkScrollableFrame(self.tab_trabajadores, label_text="Nómina Registrada")
        self.frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def guardar_trabajador(self):
        # Aquí conectaremos con la función de la DB
        cedula = self.entry_cedula.get()
        nombre = self.entry_nombre.get()
        
        if not cedula or not nombre:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return

        # Generamos el UUID para este nuevo registro
        id_seguro = str(uuid.uuid4())
        
        # Mensaje de confirmación (Luego lo cambiaremos por el INSERT real)
        CTkMessagebox(title="Éxito", message=f"Trabajador registrado con UUID: {id_seguro[:8]}...", icon="check")
        
app = ModuloMaestro()
app.mainloop()