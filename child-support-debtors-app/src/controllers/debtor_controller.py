class DebtorController:
    def __init__(self, debtor_model, view, storage_service):
        self.debtor_model = debtor_model
        self.view = view
        self.storage_service = storage_service

    def add_debtor(self, debtor_data):
        debtor = self.debtor_model(**debtor_data)
        self.storage_service.save_debtor(debtor)

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