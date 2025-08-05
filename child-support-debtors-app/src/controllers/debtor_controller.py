import re
import datetime
from models.debtor import Debtor  # Asegúrate de importar la clase


class DebtorController:
    def __init__(self, debtor_model, view, storage_service):
        self.debtor_model = debtor_model
        self.view = view
        self.storage_service = storage_service

    def validate_debtor_data(self, data):
        # 1. Apellido paterno
        if len(data["Apellido Paterno"]) > 30:
            return False, "Apellido paterno no puede exceder 30 caracteres."
        # 2. Apellido materno
        if len(data["Apellido Materno"]) > 30:
            return False, "Apellido materno no puede exceder 30 caracteres."
        # 3. Nombres
        if len(data["Nombres"]) > 50:
            return False, "Nombres no puede exceder 50 caracteres."
        # 4. Tipo de documento
        tipos_validos = ["DNI", "Carne de Extranjeria", "Pasaporte", "Otros"]
        if data["Tipo Documento"] not in tipos_validos:
            return False, "Tipo de documento inválido."
        # 5. Nro de documento
        nro_doc = data["Nro Documento"]
        tipo_doc = data["Tipo Documento"]
        if tipo_doc == "DNI":
            if not (nro_doc.isdigit() and len(nro_doc) == 8):
                return False, "DNI debe tener 8 dígitos numéricos."
        else:
            if len(nro_doc) > 12:
                return False, "Nro de documento no puede exceder 12 caracteres."
        # 6. Fecha de registro
        if not re.match(r"\d{2}-\d{2}-\d{4}$", data["Fecha Registro"]):
            return False, "Fecha de registro debe tener formato DD-MM-AAAA."
        # 7. Nro de expediente
        if not re.match(r"\d{4}-\d{4}$", data["Nro Expediente Judicial"]):
            return False, "Nro de expediente debe tener formato NNNN-YYYY."
        # 8. Pensión mensual
        try:
            pension = float(data["Pensión Mensual"])
            if pension <= 0 or len(str(int(pension))) > 15:
                return False, "Pensión mensual debe ser mayor a 0 y hasta 15 dígitos."
        except:
            return False, "Pensión mensual debe ser numérica."
        # 9. Importe adeudado
        try:
            adeudado = float(data["Importe Adeudado"])
            if adeudado <= 0 or len(str(int(adeudado))) > 15:
                return False, "Importe adeudado debe ser mayor a 0 y hasta 15 dígitos."
        except:
            return False, "Importe adeudado debe ser numérico."
        # 10. Nombre demandante
        if len(data["Demandante"]) > 100:
            return False, "Nombre demandante no puede exceder 100 caracteres."
        return True, ""

    def add_debtor(self, debtor_data):
        valid, msg = self.validate_debtor_data(debtor_data)
        if not valid:
            if self.view:
                self.view.show_error(msg)
            return False
        mapped_data = {
            "apellido_paterno": debtor_data["Apellido Paterno"],
            "apellido_materno": debtor_data["Apellido Materno"],
            "nombres": debtor_data["Nombres"],
            "tipo_documento": debtor_data["Tipo Documento"],
            "nro_documento": debtor_data["Nro Documento"],
            "fecha_registro": debtor_data["Fecha Registro"],
            "nro_expediente": debtor_data["Nro Expediente Judicial"],
            "pension_mensual": debtor_data["Pensión Mensual"],
            "importe_adeudado": debtor_data["Importe Adeudado"],
            "nombre_demandante": debtor_data["Demandante"]
        }
        debtor = Debtor(**mapped_data)
        self.storage_service.save_debtor(debtor)
        return True  # Puedes retornar True para indicar éxito

    def search_debtors(self, search_criteria):
        debtors = self.storage_service.load_debtors()
        filtered_debtors = self._filter_debtors(debtors, search_criteria)
        return filtered_debtors

    def get_debtor_details(self, debtor_id):
        debtors = self.storage_service.load_debtors()
        for debtor in debtors:
            if debtor.id == debtor_id:
                return debtor
        return None

    def _filter_debtors(self, debtors, criteria):
        # Implement filtering logic based on criteria
        filtered = []
        for debtor in debtors:
            if self._matches_criteria(debtor, criteria):
                filtered.append(debtor)
        return filtered

    def _matches_criteria(self, debtor, criteria):
        # Implement matching logic for debtor based on criteria
        return True  # Placeholder for actual matching logic

    def handle_user_request(self, request):
        # Handle requests from the view
        pass  # Placeholder for handling user requests

    def get_all_debtors(self):
        return self.storage_service.load_debtors()

    def search_by_names(self, ap_paterno, ap_materno, nombres):
        debtors = self.storage_service.load_debtors()
        filtered = []
        for debtor in debtors:
            if (
                (ap_paterno and ap_paterno.lower() in debtor.apellido_paterno.lower()) or
                (ap_materno and ap_materno.lower() in debtor.apellido_materno.lower()) or
                (nombres and nombres.lower() in debtor.nombres.lower())
            ):
                filtered.append(debtor)
        return filtered

    def search_by_document(self, tipo_doc, nro_doc):
        debtors = self.storage_service.load_debtors()
        filtered = []
        for debtor in debtors:
            if (
                debtor.tipo_documento == tipo_doc and
                debtor.nro_documento == nro_doc
            ):
                filtered.append(debtor)
        return filtered

    def search_by_period(self, fecha_inicio, fecha_fin):
        # fecha_inicio y fecha_fin en formato "DD-MM-YYYY"
        debtors = self.storage_service.load_debtors()
        filtered = []
        fi = datetime.datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
        ff = datetime.datetime.strptime(fecha_fin, "%d-%m-%Y").date()
        for debtor in debtors:
            try:
                fr = datetime.datetime.strptime(debtor.fecha_registro, "%d-%m-%Y").date()
                if fi <= fr <= ff:
                    filtered.append(debtor)
            except Exception:
                continue
        return filtered