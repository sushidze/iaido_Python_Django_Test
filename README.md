# iaido_Python_Django_Test

## Features

- Create, retrieve, update, and delete person records
- Filter persons based on various criteria
- User authentication using username and password
- Token-based authentication for API access
- Pagination for large result sets

## Installation

1. Clone the repository:
   ```shell
   git clone git@github.com:sushidze/iaido_Python_Django_Test.git
   ```
   
2. Create and activate virtual environment:

    ```shell
    python -m venv env
    ```

    ```shell
    source env/bin/activate
    ```

3. Install the required dependencies:
   ```shell
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```shell
   python manage.py migrate
   ```
   
5. (Optional) Create a superuser account to access the admin interface:

   ```shell
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```shell
   python manage.py runserver
   ```

9. The application should now be accessible at `http://127.0.0.1:8000/`. You can use tools like Postman to interact with the API endpoints.

## API Endpoints

- **GET /api/persons/** - Retrieve a list of all persons
- **POST /api/persons/** - Create a new person
- **GET /api/persons/{id}/** - Retrieve details of a specific person
- **PUT /api/persons/{id}/** - Update details of a specific person
- **DELETE /api/persons/{id}/** - Delete a specific person
- **GET /api/persons/filtered_persons/** - Retrieve filtered list of persons
- **POST /login/** - Login to the app
- **POST /api-token-auth/** - Obtain an authentication token by providing username and password

Please note that some endpoints may require authentication.
