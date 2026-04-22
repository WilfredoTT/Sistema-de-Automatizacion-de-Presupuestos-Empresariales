import ctypes
from database import inicializar_db
from gui.login import LoginWindow 

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('tedimeca.erp.v1')
except:
    pass

if __name__ == "__main__":
    inicializar_db()#creación de la base de datos y el usuario default si no existe
    loginwindow = LoginWindow()
    loginwindow.mainloop()