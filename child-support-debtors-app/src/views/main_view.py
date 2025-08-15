import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import re

class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.debtor_list = []
        self.selected_debtor = None

        self.root = tk.Tk()
        self.root.title("App Deuda Alimentaria")

        # --- Search Section ---
        self.search_type = tk.IntVar(value=1)
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)

        # Radiobuttons
        tk.Radiobutton(search_frame, text="Por nombres y apellidos", variable=self.search_type, value=1, command=self.render_search_fields).grid(row=0, column=0, sticky="w")
        tk.Radiobutton(search_frame, text="Por documento", variable=self.search_type, value=2, command=self.render_search_fields).grid(row=0, column=1, sticky="w")
        tk.Radiobutton(search_frame, text="Por periodo", variable=self.search_type, value=3, command=self.render_search_fields).grid(row=0, column=2, sticky="w")

        # Dynamic search fields frame
        self.dynamic_search_frame = tk.Frame(self.root)
        self.dynamic_search_frame.pack(pady=5)
        self.render_search_fields()

        tk.Button(self.root, text="Buscar", command=self.handle_search_btn).pack(pady=5)

        # Add new debtor button
        tk.Button(self.root, text="Cargar nuevo deudor", command=self.handle_add_debtor_btn).pack(pady=5)

        # Debtor list
        self.tree = ttk.Treeview(self.root, columns=("ap_paterno", "ap_materno", "nombres", "tipo_doc", "nro_doc", "fecha_registro"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.replace("_", " ").title())
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Details section
        self.details_text = tk.Text(self.root, height=10, width=60)
        self.details_text.pack(pady=10)

    def render_search_fields(self):
        # Clear previous widgets
        for widget in self.dynamic_search_frame.winfo_children():
            widget.destroy()
        self.search_fields = {}

        if self.search_type.get() == 1:
            # Buscar por nombres y apellidos
            tk.Label(self.dynamic_search_frame, text="Apellido Paterno:").grid(row=0, column=0)
            self.search_fields["ap_paterno"] = tk.Entry(self.dynamic_search_frame)
            self.search_fields["ap_paterno"].grid(row=0, column=1)
            tk.Label(self.dynamic_search_frame, text="Apellido Materno:").grid(row=1, column=0)
            self.search_fields["ap_materno"] = tk.Entry(self.dynamic_search_frame)
            self.search_fields["ap_materno"].grid(row=1, column=1)
            tk.Label(self.dynamic_search_frame, text="Nombres:").grid(row=2, column=0)
            self.search_fields["nombres"] = tk.Entry(self.dynamic_search_frame)
            self.search_fields["nombres"].grid(row=2, column=1)
        elif self.search_type.get() == 2:
            # Buscar por documento
            tk.Label(self.dynamic_search_frame, text="Tipo Documento:").grid(row=0, column=0)
            self.search_fields["tipo_doc"] = ttk.Combobox(self.dynamic_search_frame, values=["DNI", "Carne de Extranjeria", "Pasaporte", "Otros"], state="readonly")
            self.search_fields["tipo_doc"].grid(row=0, column=1)
            self.search_fields["tipo_doc"].current(0)
            tk.Label(self.dynamic_search_frame, text="Nro Documento:").grid(row=1, column=0)
            self.search_fields["nro_doc"] = tk.Entry(self.dynamic_search_frame)
            self.search_fields["nro_doc"].grid(row=1, column=1)
        elif self.search_type.get() == 3:
            # Buscar por periodo
            tk.Label(self.dynamic_search_frame, text="Fecha Inicio:").grid(row=0, column=0)
            self.search_fields["fecha_inicio"] = DateEntry(self.dynamic_search_frame, date_pattern="dd-mm-yyyy", maxdate=datetime.date.today())
            self.search_fields["fecha_inicio"].grid(row=0, column=1)
            tk.Label(self.dynamic_search_frame, text="Fecha Fin:").grid(row=1, column=0)
            self.search_fields["fecha_fin"] = DateEntry(self.dynamic_search_frame, date_pattern="dd-mm-yyyy", maxdate=datetime.date.today())
            self.search_fields["fecha_fin"].grid(row=1, column=1)

    def display_debtor_list(self):
        self.tree.delete(*self.tree.get_children())
        for debtor in self.debtor_list:
            self.tree.insert("", tk.END, values=(
                debtor.apellido_paterno,
                debtor.apellido_materno,
                debtor.nombres,
                debtor.tipo_documento,
                debtor.nro_documento,
                debtor.fecha_registro
            ))

    def handle_search_btn(self):
        print("Botón de búsqueda presionado")
        print("Campos actuales:", self.search_fields)
        tipo = self.search_type.get()
        if tipo == 1:
            ap_paterno = self.search_fields["ap_paterno"].get().strip()
            ap_materno = self.search_fields["ap_materno"].get().strip()
            nombres = self.search_fields["nombres"].get().strip()
            if not (ap_paterno or ap_materno or nombres):
                messagebox.showerror("Error", "Debe ingresar al menos uno de los campos.")
                return
            self.debtor_list = self.controller.search_by_names(ap_paterno, ap_materno, nombres)
        elif tipo == 2:
            tipo_doc = self.search_fields["tipo_doc"].get()
            nro_doc = self.search_fields["nro_doc"].get().strip()
            # Validación igual que en add_debtor
            if tipo_doc == "DNI":
                if not (nro_doc.isdigit() and len(nro_doc) == 8):
                    messagebox.showerror("Error", "DNI debe tener 8 dígitos numéricos.")
                    return
            else:
                if len(nro_doc) > 12 or not nro_doc:
                    messagebox.showerror("Error", "Nro de documento no puede exceder 12 caracteres y es requerido.")
                    return
            self.debtor_list = self.controller.search_by_document(tipo_doc, nro_doc)
        elif tipo == 3:
            fecha_inicio = self.search_fields["fecha_inicio"].get_date()
            fecha_fin = self.search_fields["fecha_fin"].get_date()
            hoy = datetime.date.today()
            if fecha_inicio > hoy or fecha_fin > hoy:
                messagebox.showerror("Error", "Las fechas no pueden ser superiores a la fecha actual.")
                return
            if fecha_inicio > fecha_fin:
                messagebox.showerror("Error", "La fecha de inicio no puede ser superior a la fecha de fin.")
                return
            self.debtor_list = self.controller.search_by_period(fecha_inicio.strftime("%d-%m-%Y"), fecha_fin.strftime("%d-%m-%Y"))

        self.details_text.config(state=tk.NORMAL)  # Habilita edición para limpiar
        self.details_text.delete("1.0", tk.END)    # Limpia el detalle
        self.details_text.config(state=tk.DISABLED)  # Deshabilita edición

        self.display_debtor_list()

    def show_debtor_details(self, debtor):
        self.details_text.config(state=tk.NORMAL)  # Habilita edición para mostrar
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
        )
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)  # Hace el detalle no editable

    def handle_add_debtor_btn(self):
        fields = [
            "Apellido Paterno", "Apellido Materno", "Nombres", "Tipo Documento",
            "Nro Documento", "Fecha Registro", "Nro Expediente Judicial",
            "Pensión Mensual", "Importe Adeudado", "Demandante"
        ]

        entries = {field: None for field in fields}

        def validate_fields(values):
            # 1. Apellido paterno
            if len(values["Apellido Paterno"]) > 30:
                return False, "Apellido paterno no puede exceder 30 caracteres."
            # 2. Apellido materno
            if len(values["Apellido Materno"]) > 30:
                return False, "Apellido materno no puede exceder 30 caracteres."
            # 3. Nombres
            if len(values["Nombres"]) > 50:
                return False, "Nombres no puede exceder 50 caracteres."
            # 4. Tipo de documento
            tipos_validos = ["DNI", "Carne de Extranjeria", "Pasaporte", "Otros"]
            if values["Tipo Documento"] not in tipos_validos:
                return False, "Tipo de documento inválido."
            # 5. Nro de documento
            nro_doc = values["Nro Documento"]
            tipo_doc = values["Tipo Documento"]
            if tipo_doc == "DNI":
                if not (nro_doc.isdigit() and len(nro_doc) == 8):
                    return False, "DNI debe tener 8 dígitos numéricos."
            else:
                if len(nro_doc) > 12:
                    return False, "Nro de documento no puede exceder 12 caracteres."
            # 6. Fecha de registro
            if not re.match(r"\d{2}-\d{2}-\d{4}$", values["Fecha Registro"]):
                return False, "Fecha de registro debe tener formato DD-MM-AAAA."
            # 7. Nro de expediente
            if not re.match(r"\d{4}-\d{4}$", values["Nro Expediente Judicial"]):
                return False, "Nro de expediente debe tener formato NNNN-YYYY."
            # 8. Pensión mensual
            try:
                pension = float(values["Pensión Mensual"])
                if pension <= 0 or len(str(int(pension))) > 15:
                    return False, "Pensión mensual debe ser mayor a 0 y hasta 15 dígitos."
            except:
                return False, "Pensión mensual debe ser numérica."
            # 9. Importe adeudado
            try:
                adeudado = float(values["Importe Adeudado"])
                if adeudado <= 0 or len(str(int(adeudado))) > 15:
                    return False, "Importe adeudado debe ser mayor a 0 y hasta 15 dígitos."
            except:
                return False, "Importe adeudado debe ser numérico."
            # 10. Nombre demandante
            if len(values["Demandante"]) > 100:
                return False, "Nombre demandante no puede exceder 100 caracteres."
            return True, ""

        def submit():
            values = {field: entries[field].get() if field != "Fecha Registro" else entries[field].get_date().strftime("%d-%m-%Y") for field in fields}
            if any(v == "" for v in values.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            valid, msg = validate_fields(values)
            if not valid:
                messagebox.showerror("Error", msg)
                return
            success = self.controller.add_debtor(values)
            if success:
                messagebox.showinfo("Éxito", "Deudor registrado correctamente.")
                self.debtor_list = self.controller.get_all_debtors()
                self.display_debtor_list()
                add_debtor_window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el deudor.")

        add_debtor_window = tk.Toplevel(self.root)
        add_debtor_window.title("Agregar Nuevo Deudor")
        add_debtor_window.geometry("400x500")  # Ancho aumentado en 100px (antes 300, ahora 400)

        for i, field in enumerate(fields):
            tk.Label(add_debtor_window, text=field).grid(row=i, column=0, padx=10, pady=10)
            if field == "Tipo Documento":
                entry = ttk.Combobox(add_debtor_window, values=["DNI", "Carne de Extranjeria", "Pasaporte", "Otros"], state="readonly")
                entry.current(0)
            elif field == "Fecha Registro":
                entry = DateEntry(add_debtor_window, date_pattern="dd-mm-yyyy")
            else:
                entry = tk.Entry(add_debtor_window)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[field] = entry

        tk.Button(add_debtor_window, text="Guardar", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            index = self.tree.index(selected)
            debtor = self.debtor_list[index]
            self.selected_debtor = debtor
            self.show_debtor_details(debtor)

    def run(self):
        self.root.mainloop()

