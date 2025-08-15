from views.main_admin_view import MainAdminView
from models.debtor import DebtorModel
from services.file_storage import FileStorage
from controllers.debtor_controller import DebtorController

def main():
    debtor_model = DebtorModel()
    storage_service = FileStorage(filename='debtors.txt')
    # La vista se instancia después del controlador, así que pásale None temporalmente
    controller = DebtorController(debtor_model, None, storage_service)
    app_admin_view = MainAdminView(controller)
    # Ahora puedes asignar la vista al controlador si lo necesitas
    controller.view = app_admin_view
    app_admin_view.run()

if __name__ == "__main__":
    main()