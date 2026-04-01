# Django MySQL Todo App

A simple Todo application built with Django and MySQL.

## Requirements

- Python 3.10+
- MySQL 8+

## Setup

1. **Clone the repo and install dependencies**

   ```bash
   pip install django mysqlclient python-dotenv
   ```

2. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   SECRET_KEY=your-secret-key
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

3. **Create the database**

   ```sql
   CREATE DATABASE your_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the dev server**

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/`

## Features

- Create, edit, and delete todos
- Mark todos as complete / undo completion
- Optional description per todo
- Admin interface at `/admin/`

## Project Structure

```
django-mysql-demo/
├── config/          # Project settings and root URLs
├── hello/           # Todo app
│   ├── migrations/
│   ├── templates/hello/
│   │   ├── base.html
│   │   ├── todo_list.html
│   │   ├── todo_form.html
│   │   └── todo_confirm_delete.html
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── manage.py
└── .env
```

## Database Schema

**`hello_todo`**

| Column        | Type          | Notes                  |
|---------------|---------------|------------------------|
| `id`          | INT (PK)      | Auto-increment         |
| `title`       | VARCHAR(255)  | Required               |
| `description` | TEXT          | Optional               |
| `completed`   | TINYINT(1)    | Default `0` (false)    |
| `created_at`  | DATETIME      | Set on create          |
| `updated_at`  | DATETIME      | Updated on every save  |
