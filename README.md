# Family Health Hub

A comprehensive health management system for tracking family medical records.

## Features

- Family member management
- Medication tracking
- Doctor information storage
- Insurance policy management
- Medical procedure tracking

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/FamilyHealthHub.git
   cd FamilyHealthHub
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000/`

## Requirements

- Python 3.8+
- Django 5.0+

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
