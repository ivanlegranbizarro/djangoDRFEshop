# Ecommerce con Django, Django REST Framework, PostgreSQL y JWT

Este proyecto es un ecommerce completo que utiliza Django, Django REST Framework, PostgreSQL y JWT para implementar un sistema de comercio electrónico con funcionalidades de autenticación y autorización.

## Rutas

    -   `admin/`: Ruta para acceder a la interfaz de administración de Django.
    -   `api/products/`: Ruta para obtener información sobre los productos disponibles en el ecommerce.
    -   `detail/<int:pk>`: Detalles de un producto específico.
    -   `new/`: Agregar un nuevo producto.
    -   `update/<int:pk>`: Actualizar un producto existente.
    -   `delete/<int:pk>`: Eliminar un producto existente.
    -   `review/<int:pk>`: Agregar una reseña para un producto específico.
    -   `review/update/<int:pk>`: Actualizar una reseña existente.
    -   `review/delete/<int:pk>`: Eliminar una reseña existente.
    -   `api/account/`: Ruta para manejar las funcionalidades de autenticación y autorización.
    -   `signup/`: Registro de un nuevo usuario.
    -   `me/`: Información del usuario autenticado.
    -   `forgot-password/`: Restablecer la contraseña.
    -   `reset-password/`: Restablecer la contraseña (confirmación).
    -   `api/order/`: Ruta para manejar los pedidos del ecommerce.
    -   `new/`: Crear un nuevo pedido.
    -   `get/`: Obtener información sobre los pedidos realizados.
    -   `get/<int:pk>/`: Detalles de un pedido específico.
    -   `delete/<int:pk>/`: Eliminar un pedido existente.
    -   `process/<int:pk>/`: Actualizar el estado de un pedido existente.

## Configuración del entorno

Para poder ejecutar este proyecto, se necesita una instancia de PostgreSQL y una versión de Python compatible con Django.

Antes de continuar, se recomienda crear un entorno virtual para instalar las dependencias necesarias:

`python -m venv myenv`
`source myenv/bin/activat`
`pip install -r requirements.txt`

Para configurar la base de datos, se deben seguir los siguientes pasos:

1.  Crear una base de datos en PostgreSQL.

2.  Configurar las credenciales de acceso a la base de datos en el archivo `settings.py`.

3.  Ejecutar las migraciones de Django para crear las tablas necesarias en la base de datos:

    Copy code

    `python manage.py makemigrations`
    `python manage.py migrate`


## Ejecutar el proyecto

Para ejecutar el proyecto, se debe activar el entorno virtual y ejecutar el servidor de Django:

  `source myenv/bin/activat`
  `python manage.py runserve`

El servidor se ejecutará en `http://localhost:8000/`.
