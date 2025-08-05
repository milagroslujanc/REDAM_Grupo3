# Child Support Debtors Application

This application is designed to manage child support debtors, allowing users to register, search, and view details of debtors in a user-friendly desktop interface. The application follows the Model-View-Controller (MVC) design pattern and utilizes object-oriented programming principles.

## Features

- Register debtors with essential information including:
  - Last names
  - First names
  - Document type
  - Document number
  - Registration date
  - Judicial file number
  - Monthly pension
  - Amount owed
  - Full name of the claimant

- Search for debtors by:
  - Names and surnames
  - Document type and number
  - Date range of registration

- Display a list of debtors and detailed information for each debtor.

## Project Structure

```
child-support-debtors-app
├── src
│   ├── models
│   │   └── debtor.py
│   ├── views
│   │   └── main_view.py
│   ├── controllers
│   │   └── debtor_controller.py
│   ├── services
│   │   └── file_storage.py
│   ├── utils
│   │   └── search.py
│   └── app.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd child-support-debtors-app
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command in the terminal:
```
python src/app.py
```

Follow the on-screen instructions to register and manage child support debtors.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.