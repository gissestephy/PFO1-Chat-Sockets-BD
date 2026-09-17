"""
Servidor de chat básico utilizando sockets TCP/IP y SQLite.

El servidor escucha conexiones en localhost:5000,
recibe mensajes enviados por los clientes, los almacena
en una base de datos SQLite y devuelve una confirmación.
"""

import socket
import sqlite3
import unicodedata
from datetime import datetime


# Configuración del servidor:
# Se utiliza localhost para que el servidor sea accesible únicamente
# desde la computadora donde se está ejecutando.
HOST = "localhost"

# Puerto utilizado para establecer la comunicación entre el cliente
# y el servidor.
PUERTO = 5000


def inicializar_db():
    """
    Crea la base de datos y la tabla de mensajes si no existen.
    """

    try:
        # Conexión con la base de datos SQLite.
        # Si el archivo chat.db no existe, SQLite lo crea automáticamente.
        conexion_db = sqlite3.connect("chat.db")

        # Creamos un cursor para ejecutar las instrucciones SQL.
        cursor = conexion_db.cursor()

        # Creamos la tabla mensajes con los campos solicitados
        # en la consigna del trabajo práctico.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)

        # Guardamos los cambios realizados en la base de datos.
        conexion_db.commit()

        # Cerramos la conexión con la base de datos.
        conexion_db.close()

        print("Base de datos inicializada correctamente.")

    except sqlite3.Error as error:
        # Si SQLite genera un error, mostramos un mensaje
        # para informar que no se pudo acceder a la base de datos.
        print(f"Error al acceder a la base de datos: {error}")


def guardar_mensaje(contenido, fecha_envio, ip_cliente):
    """
    Guarda un mensaje recibido en la base de datos SQLite.
    """

    try:
        # Abrimos la conexión con la base de datos.
        conexion_db = sqlite3.connect("chat.db")

        # Creamos un cursor para ejecutar la consulta SQL.
        cursor = conexion_db.cursor()

        # Insertamos el mensaje junto con la fecha de envío
        # y la dirección IP del cliente.
        cursor.execute("""
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        """, (contenido, fecha_envio, ip_cliente))

        # Guardamos los cambios realizados en la base de datos.
        conexion_db.commit()

        # Cerramos la conexión.
        conexion_db.close()

        print("Mensaje guardado correctamente en la base de datos.")

    except sqlite3.Error as error:
        # Si ocurre un error al guardar el mensaje,
        # informamos el problema sin detener todo el servidor.
        print(f"Error al guardar el mensaje: {error}")


def inicializar_socket():
    """
    Crea y configura el socket TCP/IP del servidor.
    """

    try:
        # Creación del socket TCP/IP.
        # AF_INET indica que se utilizará IPv4.
        # SOCK_STREAM indica que se utilizará el protocolo TCP.
        socket_servidor = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        # Asociamos el socket con la dirección y el puerto configurados.
        socket_servidor.bind((HOST, PUERTO))

        # El servidor comienza a escuchar conexiones entrantes.
        socket_servidor.listen()

        print(f"Servidor escuchando en {HOST}:{PUERTO}")

        return socket_servidor

    except OSError as error:
        # Este error puede producirse, por ejemplo,
        # si el puerto 5000 ya está siendo utilizado.
        print(f"Error al iniciar el servidor: {error}")

        return None


def aceptar_conexion(servidor):
    """
    Acepta una conexión entrante de un cliente.
    """

    # accept() espera hasta que un cliente se conecte
    # y devuelve la conexión y la dirección del cliente.
    conexion, direccion = servidor.accept()

    print(f"Cliente conectado desde: {direccion}")

    return conexion, direccion


def recibir_mensaje(conexion):
    """
    Recibe un mensaje enviado por el cliente y lo convierte
    de bytes a texto.
    """

    # Recibimos hasta 1024 bytes enviados por el cliente.
    datos = conexion.recv(1024)

    # Si no recibimos datos, significa que el cliente
    # cerró la conexión.
    if not datos:
        return None

    # Los datos recibidos por el socket están en bytes.
    # decode() los convierte nuevamente a texto.
    return datos.decode("utf-8")


# Inicializamos la base de datos antes de comenzar
# a recibir conexiones de los clientes.
inicializar_db()


# Inicializamos el socket del servidor.
servidor = inicializar_socket()


# Verificamos si el socket pudo iniciarse correctamente.
# Si el puerto está ocupado u ocurre otro error,
# inicializar_socket() devuelve None.
if servidor is None:
    print("El servidor no pudo iniciarse.")
    exit()


# Aceptamos la conexión de un cliente utilizando
# la función encargada de aceptar conexiones.
conexion, direccion = aceptar_conexion(servidor)


# Mantenemos la conexión abierta para poder recibir
# múltiples mensajes del mismo cliente.
while True:

    # Recibimos un mensaje utilizando la función encargada
    # de recibir y decodificar los datos.
    mensaje = recibir_mensaje(conexion)

    # Si el cliente cerró la conexión, finalizamos el ciclo.
    if mensaje is None:
        break

    print(f"Mensaje recibido: {mensaje}")

    # Normalizamos el texto para que "éxito", "Éxito", "exito",
    # "EXITO", etc. sean reconocidos como la misma palabra.
    mensaje_normalizado = unicodedata.normalize(
        "NFD",
        mensaje
    ).encode("ascii", "ignore").decode("utf-8").lower()

    # Si el cliente escribe "éxito", "exito", "Éxito", etc.,
    # finalizamos la comunicación.
    if mensaje_normalizado == "exito":
        break

    # Obtenemos la fecha y hora actual para registrar
    # cuándo fue recibido el mensaje.
    fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Obtenemos la dirección IP del cliente.
    # direccion contiene la IP y el puerto utilizados
    # por el cliente para establecer la conexión.
    ip_cliente = direccion[0]

    # Guardamos el mensaje recibido en la base de datos.
    guardar_mensaje(mensaje, fecha_envio, ip_cliente)

    # Enviamos una respuesta al cliente indicando que
    # el mensaje fue recibido correctamente.
    respuesta = f"Mensaje recibido: {fecha_envio}"

    # Los sockets trabajan con bytes, por eso convertimos
    # la respuesta de texto a bytes utilizando encode().
    conexion.sendall(respuesta.encode("utf-8"))


# Cerramos la conexión con el cliente.
conexion.close()
print("Conexión con el cliente cerrada.")

# Cerramos el socket del servidor.
servidor.close()
print("Servidor cerrado.")
