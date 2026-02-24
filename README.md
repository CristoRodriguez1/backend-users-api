## Backend Users API (FastAPI)

API REST de usuarios construida con **FastAPI**, **SQLAlchemy** y **SQLite**, organizada por capas (`models`, `schemas`, `crud`, `database`, `main`).

### Estructura

- `backend_users/`
  - `__init__.py`
  - `app/`
    - `__init__.py`
    - `database.py`
    - `models.py`
    - `schemas.py`
    - `crud.py`
    - `main.py`

### Instalación

```bash
cd "c:\Users\LENOVO\Documents\UNIVERSIDAD\PERSONAL\Proyecto Personal 1"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Ejecución

```bash
uvicorn backend_users.app.main:app --reload
```

La base de datos SQLite `users.db` se creará automáticamente en el directorio del proyecto.

### Endpoints principales

- `POST /users` – Crear usuario.
- `GET /users` – Listar usuarios.
- `GET /users/{id}` – Obtener usuario por id.
- `PUT /users/{id}` – Actualizar usuario.
- `DELETE /users/{id}` – Eliminar usuario.
- `POST /login` – Validar credenciales (login).

Puedes probar todo desde la documentación interactiva en `/docs`.

