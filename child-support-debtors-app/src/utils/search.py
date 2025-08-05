def search_debtors_by_name(debtors, first_name, last_name):
    return [debtor for debtor in debtors if debtor.first_name.lower() == first_name.lower() and debtor.last_name.lower() == last_name.lower()]

def search_debtors_by_document(debtors, document_type, document_number):
    return [debtor for debtor in debtors if debtor.document_type == document_type and debtor.document_number == document_number]

def search_debtors_by_date_range(debtors, start_date, end_date):
    return [debtor for debtor in debtors if start_date <= debtor.registration_date <= end_date]