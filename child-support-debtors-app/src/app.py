from views.main_view import MainView
from models.debtor import DebtorModel
from services.file_storage import FileStorage
from controllers.debtor_controller import DebtorController

def main():
    debtor_model = DebtorModel()
    storage_service = FileStorage(filename='debtors.txt')
    # La vista se instancia después del controlador, así que pásale None temporalmente
    controller = DebtorController(debtor_model, None, storage_service)
    app_view = MainView(controller)
    # Ahora puedes asignar la vista al controlador si lo necesitas
    controller.view = app_view
    app_view.run()

if __name__ == "__main__":
    main()