class Debtor:
    def __init__(self, apellido_paterno, apellido_materno, nombres, tipo_documento, nro_documento,
                 fecha_registro, nro_expediente, pension_mensual, importe_adeudado, nombre_completo_demandante):
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.nombres = nombres
        self.tipo_documento = tipo_documento
        self.nro_documento = nro_documento
        self.fecha_registro = fecha_registro
        self.nro_expediente = nro_expediente
        self.pension_mensual = pension_mensual
        self.importe_adeudado = importe_adeudado
        self.nombre_completo_demandante = nombre_completo_demandante

    def __str__(self):
        return (f"Deudor: {self.apellido_paterno} {self.apellido_materno}, {self.nombres}\n"
                f"Tipo Documento: {self.tipo_documento}, Nro Documento: {self.nro_documento}\n"
                f"Fecha de Registro: {self.fecha_registro}, Nro Expediente: {self.nro_expediente}\n"
                f"Pensión Mensual: {self.pension_mensual}, Importe Adeudado: {self.importe_adeudado}\n"
                f"Demandante: {self.nombre_completo_demandante}")