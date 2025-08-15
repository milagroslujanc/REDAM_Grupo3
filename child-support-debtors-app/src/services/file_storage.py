class FileStorage:
    def __init__(self, filename):
        self.filename = filename

    def save_debtor(self, debtor):
        with open(self.filename, 'a') as file:  # 'a' para agregar, no sobrescribir
            file.write(f"{debtor.apellido_paterno},{debtor.apellido_materno},{debtor.nombres},"
                       f"{debtor.tipo_documento},{debtor.nro_documento},{debtor.fecha_registro},"
                       f"{debtor.nro_expediente},{debtor.pension_mensual},{debtor.importe_adeudado},"
                       f"{debtor.nombre_demandante}\n")

    def load_debtors(self):
        from models.debtor import Debtor
        debtors = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 10:
                        debtor = Debtor(
                            apellido_paterno=parts[0],
                            apellido_materno=parts[1],
                            nombres=parts[2],
                            tipo_documento=parts[3],
                            nro_documento=parts[4],
                            fecha_registro=parts[5],
                            nro_expediente=parts[6],
                            pension_mensual=parts[7],
                            importe_adeudado=parts[8],
                            nombre_demandante=parts[9],
                            ultima_modificacion=parts[10] if len(parts) > 10 else ""
                        )
                        debtors.append(debtor)
        except FileNotFoundError:
            pass  # File does not exist, return empty list
        return debtors

    def save_all_debtors(self, debtors):
        with open(self.filename, 'w', encoding='utf-8') as file:
            for debtor in debtors:
                file.write(f"{debtor.apellido_paterno},{debtor.apellido_materno},{debtor.nombres},"
                           f"{debtor.tipo_documento},{debtor.nro_documento},{debtor.fecha_registro},"
                           f"{debtor.nro_expediente},{debtor.pension_mensual},{debtor.importe_adeudado},"
                           f"{debtor.nombre_demandante},{debtor.ultima_modificacion or ''}\n")