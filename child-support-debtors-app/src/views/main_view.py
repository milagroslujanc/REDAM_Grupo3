import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime

class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.debtor_list = []
        self.selected_debtor = None

        self.root = tk.Tk()
        self.root.title("Deudores Alimentarios Morosos")
        self.root.configure(bg="#fff")

        # Ventana inicia 100px más arriba
        self.root.update_idletasks()
        width = 1350
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)   # 100px más arriba
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Estilos personalizados
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("TNotebook.Tab", font=("Arial", 12, "bold"), padding=[20, 10])
        style.configure("TButton", font=("Arial", 12, "bold"), background="#9a1413", foreground="white", padding=10)
        style.map("TButton", background=[("active", "#b71c1c")])
        style.configure("TLabel", font=("Arial", 12), background="#fff", foreground="#9a1413", padding=10)
        style.configure("TEntry", font=("Arial", 12), padding=10)
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#9a1413", foreground="white")

        # Título principal
        tk.Label(self.root, text="Deudores Alimentarios Morosos", font=("Arial", 20, "bold"), fg="#9a1413", bg="#fff").pack(pady=(10, 5))  # margen superior/inferior reducido a la mitad

        # Notebook para tabs de búsqueda
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=5, padx=30, fill="x")  # margen superior/inferior reducido a la mitad

        # --- Tab 1: Nombres y Apellidos ---
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="NOMBRES Y APELLIDOS")
        self._build_tab_nombres(tab1)

        # --- Tab 2: Documento de Identidad ---
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="DOCUMENTO DE IDENTIDAD")
        self._build_tab_documento(tab2)

        # --- Tab 3: Rango de Periodos ---
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="RANGO DE PERIODOS")
        self._build_tab_periodo(tab3)

        # Botón consultar (mitad de alto y margen)
        self.btn_buscar = ttk.Button(self.root, text="CONSULTAR", command=self.handle_search_btn)
        self.btn_buscar.pack(pady=10, ipadx=30, ipady=5)  # ipady y pady a la mitad

        # Frame para la tabla y scroll
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=5, fill=tk.BOTH, expand=True)  # margen reducido a la mitad

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ap_paterno", "ap_materno", "nombres", "tipo_doc", "nro_doc", "fecha_registro"),
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

        # Vincula el evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Área de detalle
        self.details_text = tk.Text(self.root, height=10, width=60, font=("Arial", 12))
        self.details_text.pack(pady=5)  # margen reducido a la mitad
        self.details_text.config(state=tk.DISABLED)

        # Vincula el cambio de pestaña para cambiar el tipo de búsqueda
        def on_tab_change(event):
            self.search_type.set(notebook.index(notebook.select()) + 1)
        notebook.bind("<<NotebookTabChanged>>", on_tab_change)
        self.search_type = tk.IntVar(value=1)

    def _build_tab_nombres(self, parent):
        self.search_fields = {}
        frame = ttk.Frame(parent)
        frame.pack(pady=20, padx=40, fill="x")
        ttk.Label(frame, text="APELLIDO PATERNO:").grid(row=0, column=0, sticky="e", pady=10)
        self.search_fields["ap_paterno"] = ttk.Entry(frame, width=30)
        self.search_fields["ap_paterno"].grid(row=0, column=1, pady=10)
        ttk.Label(frame, text="APELLIDO MATERNO:").grid(row=1, column=0, sticky="e", pady=10)
        self.search_fields["ap_materno"] = ttk.Entry(frame, width=30)
        self.search_fields["ap_materno"].grid(row=1, column=1, pady=10)
        ttk.Label(frame, text="NOMBRES:").grid(row=2, column=0, sticky="e", pady=10)
        self.search_fields["nombres"] = ttk.Entry(frame, width=30)
        self.search_fields["nombres"].grid(row=2, column=1, pady=10)

    def _build_tab_documento(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(pady=20, padx=40, fill="x")
        ttk.Label(frame, text="TIPO DOCUMENTO:").grid(row=0, column=0, sticky="e", pady=10)
        self.search_fields["tipo_doc"] = ttk.Combobox(frame, values=["DNI", "Carne de Extranjeria", "Pasaporte", "Otros"], state="readonly", width=27)
        self.search_fields["tipo_doc"].grid(row=0, column=1, pady=10)
        self.search_fields["tipo_doc"].current(0)
        ttk.Label(frame, text="NRO DOCUMENTO:").grid(row=1, column=0, sticky="e", pady=10)
        self.search_fields["nro_doc"] = ttk.Entry(frame, width=30)
        self.search_fields["nro_doc"].grid(row=1, column=1, pady=10)

    def _build_tab_periodo(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(pady=20, padx=40, fill="x")
        ttk.Label(frame, text="FECHA INICIO:").grid(row=0, column=0, sticky="e", pady=10)
        self.search_fields["fecha_inicio"] = DateEntry(frame, date_pattern="dd-mm-yyyy", maxdate=datetime.date.today(), width=28)
        self.search_fields["fecha_inicio"].grid(row=0, column=1, pady=10)
        ttk.Label(frame, text="FECHA FIN:").grid(row=1, column=0, sticky="e", pady=10)
        self.search_fields["fecha_fin"] = DateEntry(frame, date_pattern="dd-mm-yyyy", maxdate=datetime.date.today(), width=28)
        self.search_fields["fecha_fin"].grid(row=1, column=1, pady=10)

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
                    debtor.fecha_registro
                )
            )

    def handle_search_btn(self):
        tipo = self.search_type.get()
        if tipo == 1:
            ap_paterno = self.search_fields["ap_paterno"].get().strip()
            ap_materno = self.search_fields["ap_materno"].get().strip()
            nombres = self.search_fields["nombres"].get().strip()
            if not (ap_paterno or ap_materno or nombres):
                messagebox.showerror("Error", "Debe ingresar al menos un apellido y un nombre.")
                return
            self.debtor_list = self.controller.search_by_names(ap_paterno, ap_materno, nombres)
        elif tipo == 2:
            tipo_doc = self.search_fields["tipo_doc"].get()
            nro_doc = self.search_fields["nro_doc"].get().strip()
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

        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)
        self.details_text.config(state=tk.DISABLED)
        self.display_debtor_list()

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            nro_doc = selected  # El iid es el nro_documento
            debtor = next((d for d in self.debtor_list if d.nro_documento == nro_doc), None)
            if debtor:
                self.selected_debtor = debtor
                self.show_debtor_details(debtor)

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
        )
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

