import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import re
import os

def validar_login():
    login_win = tk.Tk()
    login_win.title("Login Administrador")
    login_win.geometry("400x220")
    tk.Label(login_win, text="Usuario:", font=("Arial", 12, "bold"), bg="#fff", fg="#9a1413", height=2).pack(pady=5)
    usuario_entry = tk.Entry(login_win, font=("Arial", 12), width=22)
    usuario_entry.pack(pady=5)
    tk.Label(login_win, text="Contraseña:", font=("Arial", 12, "bold"), bg="#fff", fg="#9a1413", height=2).pack(pady=5)
    password_entry = tk.Entry(login_win, show="*", font=("Arial", 12), width=22)
    password_entry.pack(pady=5)

    def check_login():
        usuario = usuario_entry.get().strip()
        password = password_entry.get().strip()
        try:
            with open("usuarios.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 2 and usuario == parts[0] and password == parts[1]:
                        login_win.destroy()
                        return True
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de usuarios no encontrado en: usuarios.txt")
        return False

    tk.Button(login_win, text="Ingresar", command=check_login, font=("Arial", 12, "bold"), bg="#9a1413", fg="white", height=2).pack(pady=10, ipadx=10, ipady=5)
    login_win.configure(bg="#fff")
    login_win.mainloop()

class MainAdminView:
    def __init__(self, controller):
        self.controller = controller
        self.debtor_list = []
        self.selected_debtor = None

        # Login antes de mostrar el panel
        validar_login()

        self.root = tk.Tk()
        self.root.title("PANEL ADMINISTRADOR")
        self.root.configure(bg="#fff")

        # Ancho aumentado en 200px (antes 900, ahora 1300)
        self.root.update_idletasks()
        width = 1350
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2) - 50  # 50px más arriba
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Estilos ttk
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("TButton", font=("Arial", 12, "bold"), background="#9a1413", foreground="white", padding=10)
        style.map("TButton", background=[("active", "#b71c1c")])
        style.configure("TLabel", font=("Arial", 12), background="#fff", foreground="#9a1413", padding=10)
        style.configure("TEntry", font=("Arial", 12), padding=10)
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#9a1413", foreground="white")

        # Título principal
        tk.Label(self.root, text="Panel Administrador de Deudores", font=("Arial", 20, "bold"), fg="#9a1413", bg="#fff", height=2).pack(pady=(20, 10))

        # --- Botones CRUD ---
        crud_frame = tk.Frame(self.root, bg="#fff")
        crud_frame.pack(pady=5)
        tk.Button(crud_frame, text="Agregar deudor", command=self.handle_add_debtor_btn, font=("Arial", 12, "bold"), bg="#9a1413", fg="white", height=2).grid(row=0, column=0, padx=5, ipadx=10, ipady=5)
        tk.Button(crud_frame, text="Editar deudor", command=self.handle_edit_debtor_btn, font=("Arial", 12, "bold"), bg="#9a1413", fg="white", height=2).grid(row=0, column=1, padx=5, ipadx=10, ipady=5)
        tk.Button(crud_frame, text="Eliminar deudor", command=self.handle_delete_debtor_btn, font=("Arial", 12, "bold"), bg="#9a1413", fg="white", height=2).grid(row=0, column=2, padx=5, ipadx=10, ipady=5)

        # Debtor list con scroll y alto de 5 filas
        tree_frame = tk.Frame(self.root, bg="#fff")
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ap_paterno", "ap_materno", "nombres", "tipo_doc", "nro_doc", "fecha_registro", "ultima_modificacion"),
            show="headings",
            height=5
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.replace("_", " ").title())
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Details section
        self.details_text = tk.Text(self.root, height=10, width=70, font=("Arial", 12))
        self.details_text.pack(pady=10)
        self.details_text.config(state=tk.DISABLED)

        self.refresh_debtor_list()

    def refresh_debtor_list(self):
        self.debtor_list = self.controller.get_all_debtors()
        self.display_debtor_list()

    def display_debtor_list(self):
        self.tree.delete(*self.tree.get_children())
        for debtor in self.debtor_list:
            self.tree.insert(
                "", tk.END,
                iid=debtor.nro_documento,  # Usa nro_documento como identificador único
                values=(
                    debtor.apellido_paterno,
                    debtor.apellido_materno,
                    debtor.nombres,
                    debtor.tipo_documento,
                    debtor.nro_documento,
                    debtor.fecha_registro,
                    getattr(debtor, "ultima_modificacion", "")
                )
            )

    def show_debtor_details(self, debtor):
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)
        details = (
            f"Apellido Paterno: {debtor.apellido_paterno}\n"
            f"Apellido Materno: {debtor.apellido_materno}\n"
            f"Nombres: {debtor.nombres}\n"
            f"Tipo Documento: {debtor.tipo_documento}\n"
            f"Nro Documento: {debtor.nro_documento}\n"
            f"Fecha Registro: {debtor.fecha_registro}\n"
            f"Nro Expediente Judicial: {debtor.nro_expediente}\n"
            f"Pensión Mensual: {debtor.pension_mensual}\n"
            f"Importe Adeudado: {debtor.importe_adeudado}\n"
            f"Demandante: {debtor.nombre_demandante}\n"
            f"Última Modificación: {getattr(debtor, 'ultima_modificacion', '')}\n"
        )
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)

    def handle_add_debtor_btn(self):
        self.open_debtor_form("Agregar")

    def handle_edit_debtor_btn(self):
        if not self.selected_debtor:
            messagebox.showerror("Error", "Seleccione un deudor para editar.")
            return
        self.open_debtor_form("Editar", self.selected_debtor)

    def handle_delete_debtor_btn(self):
        if not self.selected_debtor:
            messagebox.showerror("Error", "Seleccione un deudor para eliminar.")
            return
        confirm = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este deudor?")
        if confirm:
            self.controller.delete_debtor(self.selected_debtor.nro_documento)
            self.refresh_debtor_list()
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete("1.0", tk.END)
            self.details_text.config(state=tk.DISABLED)
            self.selected_debtor = None

    def open_debtor_form(self, modo, debtor=None):
        fields = [
            "Apellido Paterno", "Apellido Materno", "Nombres", "Tipo Documento",
            "Nro Documento", "Fecha Registro", "Nro Expediente Judicial",
            "Pensión Mensual", "Importe Adeudado", "Demandante"
        ]
        entries = {}

        form = tk.Toplevel(self.root)
        form.title(f"{modo} Deudor")
        form.geometry("520x750")  # +100px de alto respecto al anterior (570+100)
        form.configure(bg="#fff")

        # Tamaños 30% más pequeños
        label_font = ("Arial", 9, "bold")
        entry_font = ("Arial", 9)
        label_height = 3  # era 4
        entry_width = 24  # era 34
        entry_ipady = 10  # era 15

        for i, field in enumerate(fields):
            tk.Label(form, text=field, height=label_height, anchor="w", font=label_font, bg="#fff", fg="#9a1413").grid(row=i, column=0, padx=10, pady=7, sticky="w")
            if field == "Tipo Documento":
                entry = ttk.Combobox(form, values=["DNI", "Carne de Extranjeria", "Pasaporte", "Otros"], state="readonly", font=entry_font, width=entry_width)
                entry.current(0)
            elif field == "Fecha Registro":
                entry = DateEntry(form, date_pattern="dd-mm-yyyy", width=entry_width)
            else:
                entry = tk.Entry(form, font=entry_font, width=entry_width)
            entry.grid(row=i, column=1, padx=10, pady=7, sticky="ew", ipady=entry_ipady)
            entries[field] = entry

        # Si es edición, carga los datos
        if modo == "Editar" and debtor:
            entries["Apellido Paterno"].insert(0, debtor.apellido_paterno)
            entries["Apellido Materno"].insert(0, debtor.apellido_materno)
            entries["Nombres"].insert(0, debtor.nombres)
            entries["Tipo Documento"].set(debtor.tipo_documento)
            entries["Nro Documento"].insert(0, debtor.nro_documento)
            try:
                fecha = datetime.datetime.strptime(debtor.fecha_registro, "%d-%m-%Y")
                entries["Fecha Registro"].set_date(fecha)
            except:
                pass
            entries["Nro Expediente Judicial"].insert(0, debtor.nro_expediente)
            entries["Pensión Mensual"].insert(0, debtor.pension_mensual)
            entries["Importe Adeudado"].insert(0, debtor.importe_adeudado)
            entries["Demandante"].insert(0, debtor.nombre_demandante)

        def submit():
            values = {field: entries[field].get() if field != "Fecha Registro" else entries[field].get_date().strftime("%d-%m-%Y") for field in fields}
            if any(v == "" for v in values.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            # Validación igual que antes...
            valid, msg = self.controller.validate_debtor_data(values)
            if not valid:
                messagebox.showerror("Error", msg)
                return
            # Agregar o editar
            values["Última Modificación"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            if modo == "Agregar":
                self.controller.add_debtor(values)
            else:
                self.controller.edit_debtor(debtor.nro_documento, values)
            self.refresh_debtor_list()
            # Actualiza el detalle si hay uno seleccionado
            if self.selected_debtor:
                for d in self.debtor_list:
                    if d.nro_documento == values["Nro Documento"]:
                        self.selected_debtor = d
                        self.show_debtor_details(d)
                        break
            form.destroy()

        tk.Button(form, text="Guardar", command=submit, font=("Arial", 12, "bold"), bg="#9a1413", fg="white", height=2).grid(row=len(fields), column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            nro_doc = selected  # El iid es el nro_documento
            debtor = next((d for d in self.debtor_list if d.nro_documento == nro_doc), None)
            if debtor:
                self.selected_debtor = debtor
                self.show_debtor_details(debtor)

    def run(self):
        self.root.mainloop()

