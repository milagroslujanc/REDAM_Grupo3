import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

def run_app():
    """Ejecuta el archivo 'app.py'."""
    try:
        # Usa subprocess para ejecutar la app.py como un proceso separado
        subprocess.Popen(['python', os.path.join('src', 'app.py')])
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'app.py'")

def run_admin_app():
    """Ejecuta el archivo 'app_admin.py'."""
    try:
        subprocess.Popen(['python', os.path.join('src', 'app_admin.py')])
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'app_admin.py'")

# --- Configuración de la Ventana Principal ---
root = tk.Tk()
root.title("Menú Principal REDAM")
root.geometry("450x250")
root.resizable(False, False)

# Paleta de colores: Gris claro y rojo
bg_color = "#e0e0e0"       
primary_color = "#b02a2a"    
text_color = "#333333"      
button_text_color = "white"

root.config(bg=bg_color)
style = ttk.Style()
style.theme_use("clam")

# Estilos
style.configure("TButton",
    background=primary_color,
    foreground=button_text_color,
    font=("Arial", 12, "bold"),
    padding=10,
    relief="flat",
    bordercolor=primary_color,
    borderwidth=1,
)
style.map("TButton",
    background=[('active', '#e63232')],
)
style.configure("TLabel",
    background=bg_color,
    foreground=text_color,
)

# --- Contenido de la Interfaz ---
frame = tk.Frame(root, bg=bg_color, padx=30, pady=30)
frame.pack(expand=True, fill="both")

title_label = tk.Label(frame, text="Menú Principal REDAM", font=("Arial", 18, "bold"), bg=bg_color, fg=primary_color)
title_label.pack(pady=10)

desc_label = tk.Label(frame, text="Seleccione la opcion de su preferencia:", font=("Arial", 12), bg=bg_color, fg=text_color)
desc_label.pack(pady=(0, 20))

button_frame = tk.Frame(frame, bg=bg_color)
button_frame.pack()

btn_app = ttk.Button(button_frame, text="Buscar Deudores", command=run_app, width=20)
btn_app.pack(side="left", padx=10)

btn_admin_app = ttk.Button(button_frame, text="Mantenimiento", command=run_admin_app, width=20)
btn_admin_app.pack(side="right", padx=10)

root.mainloop()