# ✅ Lista de tareas con Flask

Aplicación web educativa de gestión de tareas desarrollada con **Python, Flask y MySQL**. Permite registrar usuarios, iniciar sesión y administrar tareas personales mediante operaciones CRUD, manteniendo los datos de cada cuenta separados.

> **Nota:** Este es un proyecto educativo orientado a practicar desarrollo Full-Stack con Flask, autenticación, formularios y persistencia de datos en MySQL. No representa un producto comercial ni pretende cubrir todos los requisitos de una aplicación de producción.

## 📸 Recorrido visual

### Acceso y registro

La aplicación permite crear una cuenta local e iniciar sesión para acceder al espacio personal de tareas.

![Formulario de inicio de sesión](<screenshots/Captura de pantalla 2026-09-29 142250.png>)

![Formulario de registro](<screenshots/Captura de pantalla 2026-09-29 142437.png>)

### Gestión de tareas

Una vez autenticado, cada usuario puede crear una nueva tarea, consultar solamente sus propios registros y acceder al formulario de edición.

![Creación de una tarea](<screenshots/Captura de pantalla 2026-09-29 142529.png>)

![Listado de tareas del usuario autenticado](<screenshots/Captura de pantalla 2026-09-29 142538.png>)

![Edición y eliminación de una tarea](<screenshots/Captura de pantalla 2026-09-29 142551.png>)

Después de eliminar una tarea, la aplicación muestra una notificación de confirmación.

![Confirmación de eliminación](<screenshots/Captura de pantalla 2026-09-29 142638.png>)

## ✨ Funcionalidades principales

- Registro de usuarios con validación de nombre y contraseña.
- Inicio y cierre de sesión.
- Creación, listado, edición y eliminación de tareas.
- Marcado de tareas como completadas.
- Listado limitado a las tareas del usuario autenticado.
- Restricción de consulta, edición y eliminación de tareas a su propietario.
- Mensajes de validación y confirmación para las operaciones principales.

## 🧰 Tecnologías utilizadas

- **Python 3**
- **Flask**
- **MySQL** mediante `mysql-connector-python`
- **python-dotenv** para cargar configuración local desde `.env`
- **HTML5** y plantillas Jinja
- **CSS** propio, sin frameworks visuales externos

## 📁 Estructura general

```text
Lista_Tarea_Flask/
├── todo/
│   ├── auth.py             # Registro, login, logout y protección de rutas
│   ├── todo.py             # CRUD y autorización de tareas
│   ├── csrf.py             # Generación y validación de tokens CSRF
│   ├── db.py               # Conexión e inicialización de MySQL
│   ├── schema.py           # Definición no destructiva de tablas
│   ├── static/style.css    # Estilos de la interfaz
│   └── templates/          # Plantillas HTML/Jinja
├── .env.example            # Variables de entorno de referencia
├── requirements.txt        # Dependencias de Python
└── screenshots/            # Capturas incluidas en este documento
```

## ⚙️ Requisitos previos

- Python 3 y `pip`.
- MySQL en ejecución y un usuario local con permisos para crear o utilizar una base de datos.
- PowerShell en Windows.

## 🚀 Instalación local

Desde la raíz del proyecto, creá y utilizá un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si preferís no activar el entorno, podés usar directamente su intérprete:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 🔐 Configuración mediante `.env`

Creá el archivo local a partir del ejemplo:

```powershell
Copy-Item .env.example .env
```

Completá `.env` con los datos de tu entorno local. No publiques este archivo: está excluido mediante `.gitignore`.

```text
FLASK_SECRET_KEY=una-clave-local-segura-y-aleatoria
FLASK_DATABASE_HOST=127.0.0.1
FLASK_DATABASE_PORT=3306
FLASK_DATABASE_USER=tu_usuario_mysql
FLASK_DATABASE_PASSWORD=tu_contraseña_mysql_local
FLASK_DATABASE=lista_tarea_flask
```

Los valores anteriores son ejemplos locales; reemplazalos por tus propias credenciales y una clave de sesión segura.

## 🗄️ Configuración de MySQL

Creá una base de datos vacía con un nombre acorde al valor configurado en `FLASK_DATABASE`:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u TU_USUARIO -p -h 127.0.0.1 -P 3306 -e "CREATE DATABASE IF NOT EXISTS lista_tarea_flask CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

Luego inicializá las tablas requeridas desde la raíz del proyecto:

```powershell
python -m flask --app todo init-db
```

El comando actual usa `CREATE TABLE IF NOT EXISTS`: crea las tablas necesarias cuando no existen y no está diseñado para eliminar datos existentes.

## ▶️ Ejecución

Con MySQL configurado y las tablas inicializadas, iniciá Flask:

```powershell
python -m flask --app todo run --debug
```

Abrí la aplicación en [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## 🔑 Autenticación y gestión de tareas

Las cuentas se almacenan en MySQL y las contraseñas se guardan mediante hash. Al iniciar sesión, Flask mantiene la sesión del usuario autenticado. Todas las rutas de tareas requieren esa sesión.

Cada tarea contiene un propietario (`created_by`). Las consultas y operaciones de actualización o eliminación incluyen el identificador del usuario autenticado, por lo que una cuenta no puede acceder a tareas de otra mediante la modificación de URLs o identificadores.

## 🛡️ Buenas prácticas de seguridad incorporadas

Estas medidas forman parte del objetivo educativo del proyecto; no implican que la aplicación esté preparada para producción sin una revisión adicional.

| Riesgo abordado | Medida incorporada |
| --- | --- |
| Exposición de contraseñas | Hash con las utilidades seguras de Werkzeug. |
| Inyección SQL | Consultas parametrizadas mediante `mysql-connector-python`. |
| CSRF | Token asociado a la sesión y validado en todas las solicitudes `POST`. |
| Acceso no autorizado | Decorador de rutas protegidas y sesión requerida para las tareas. |
| Acceso a tareas ajenas | Filtro por `id` y `created_by` en la obtención, edición y eliminación. |
| Configuración sensible | Credenciales de MySQL y clave de sesión obtenidas desde variables de entorno. |

## ✅ Estado actual

Se verificaron manualmente el registro, inicio y cierre de sesión, creación, edición y eliminación de tareas, y la separación de tareas entre dos usuarios distintos. La aplicación cuenta además con dependencias declaradas, inicialización no destructiva de tablas y configuración local mediante `.env`.

