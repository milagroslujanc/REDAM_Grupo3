class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.debtor_list = []
        self.selected_debtor = None

    def display_debtor_list(self):
        # Code to display the list of debtors in the GUI
        pass

    def show_debtor_details(self, debtor):
        # Code to display the details of the selected debtor in the GUI
        pass

    def handle_search(self, search_criteria):
        # Code to handle user search input and update the debtor list
        self.debtor_list = self.controller.search_debtors(search_criteria)
        self.display_debtor_list()

    def on_debtor_selected(self, debtor):
        self.selected_debtor = debtor
        self.show_debtor_details(debtor)

    def run(self):
        # Code to start the GUI event loop
        pass