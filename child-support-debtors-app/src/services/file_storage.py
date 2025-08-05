class FileStorage:
    def __init__(self, filename):
        self.filename = filename

    def save_debtors(self, debtors):
        with open(self.filename, 'w') as file:
            for debtor in debtors:
                file.write(f"{debtor.last_name_paterno},{debtor.last_name_materno},{debtor.first_name},"
                           f"{debtor.document_type},{debtor.document_number},{debtor.registration_date},"
                           f"{debtor.judicial_file_number},{debtor.monthly_pension},{debtor.amount_owed},"
                           f"{debtor.claimant_full_name}\n")

    def load_debtors(self):
        debtors = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    last_name_paterno, last_name_materno, first_name, document_type, document_number, \
                    registration_date, judicial_file_number, monthly_pension, amount_owed, claimant_full_name = line.strip().split(',')
                    debtor = {
                        'last_name_paterno': last_name_paterno,
                        'last_name_materno': last_name_materno,
                        'first_name': first_name,
                        'document_type': document_type,
                        'document_number': document_number,
                        'registration_date': registration_date,
                        'judicial_file_number': judicial_file_number,
                        'monthly_pension': float(monthly_pension),
                        'amount_owed': float(amount_owed),
                        'claimant_full_name': claimant_full_name
                    }
                    debtors.append(debtor)
        except FileNotFoundError:
            pass  # File does not exist, return empty list
        return debtors