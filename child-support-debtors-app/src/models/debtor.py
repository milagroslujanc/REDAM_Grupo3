class Debtor:
    def __init__(
        self,
        apellido_paterno,
        apellido_materno,
        nombres,
        tipo_documento,
        nro_documento,
        fecha_registro,
        nro_expediente,
        pension_mensual,
        importe_adeudado,
        nombre_demandante
    ):
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.nombres = nombres
        self.tipo_documento = tipo_documento
        self.nro_documento = nro_documento
        self.fecha_registro = fecha_registro
        self.nro_expediente = nro_expediente
        self.pension_mensual = pension_mensual
        self.importe_adeudado = importe_adeudado
        self.nombre_demandante = nombre_demandante

class DebtorModel:
    def __init__(self):
        self.debtors = []

    def add_debtor(self, debtor):
        self.debtors.append(debtor)

    def get_debtors(self):
        return self.debtors

    def find_debtor_by_document(self, nro_documento):
        for debtor in self.debtors:
            if debtor.nro_documento == nro_documento:
                return debtor
        return None

    def remove_debtor(self, nro_documento):
        self.debtors = [d for d in self.debtors if d.nro_documento != nro_documento]

    def clear_debtors(self):
        self.debtors.clear()

