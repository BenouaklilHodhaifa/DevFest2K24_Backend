You can enhance your README by using tables, emojis, and some additional formatting for clarity. Here's a styled version with a table, relevant emojis, and some structured headings:

---

# 🏭 Factory 86 Backend

This Django-based backend manages the data needs for the Factory 86 factory management application.

## 📂 Repository Structure

| Folder / File | Description |
|---------------|-------------|
| :file_folder: **DevFest2k24_Backend/** | The default folder created with the Django project. Its most important files are: |
| :page_facing_up: **settings.py** | Global settings for the project. |
| :page_facing_up: **urls.py** | Main URL dispatcher, currently redirects all URLs to the `main/` app. |
| :file_folder: **main/** | The primary app of the Django project. The key files and folders are: |
| :page_facing_up: **models.py** | Defines models that interface with the database, such as `StampingPress`, `PaintingRobot`, and `AGV` (all inherit from `django.models.Model`). |
| :page_facing_up: **serializers.py** | Contains class-based serializers inherited from `Django Rest Framework ModelSerializer`. They convert between complex Django Model instances and native Python data types. |
| :page_facing_up: **urls.py** | Local URL dispatcher for the `main/` app, linking endpoints to the appropriate views. |
| :file_folder: **views/** | Contains views that handle requests. The views are categorized by different concerns: |
| :page_facing_up: **sensors_loading.py** | Handles POST requests from sensors, storing their data in the database. Each sensor type has a dedicated view. |
| :page_facing_up: **sensors_uploading.py** | Provides logged sensor data to the frontend. |
| :page_facing_up: **account.py** | Manages account-related operations, such as account listing. |
| :page_facing_up: **notification.py** | Retrieves logged notifications from the database and sends them in real time. |
| :page_facing_up: **task.py** | Manages automatic task logic, such as listing tasks and updating their statuses. |
| :page_facing_up: **team.py** | Handles logic related to operator teams. |

---

## 🏃 Runing the server
Once cloned, create a python or conda virtual environment, install the dependencies in requirements.txt, and then follow the steps to launch the server :
1. Our repo is configured to work with PostGRES, so create a new PostGRES database, and copy the credentials in a .env file in the root directory of the repo like so:
```yaml
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```
2. in the root folder run : python manage.py makemigrations
3. in the root folder run : python manage.py migrate
4. in the root folder launch a local development server with : python manage.py runserver

## ⚙️ API Documentation
The API documentation can be found on the postman project at the following link : 
