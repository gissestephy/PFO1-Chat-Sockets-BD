"""
Cliente de chat básico utilizando sockets TCP/IP.

El cliente se conecta al servidor, permite enviar múltiples
mensajes y muestra la respuesta recibida del servidor.
"""

import socket
import unicodedata


# Configuración del servidor al que se conectará el cliente.
# localhost indica que el servidor está ejecutándose
# en la misma computadora.
HOST = "localhost"

# Puerto utilizado por el servidor para recibir conexiones.
PUERTO = 5000


# Creamos el socket utilizando IPv4 y TCP.
cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)


# Conectamos el cliente con el servidor utilizando
# la dirección y el puerto configurados.
cliente.connect((HOST, PUERTO))

print("Conexión establecida con el servidor.")


# El cliente permanece dentro del ciclo para poder
# enviar múltiples mensajes.
while True:

    # Solicitamos al usuario que escriba un mensaje.
    mensaje = input("Escribí un mensaje: ")

    # Normalizamos el texto para que "éxito", "Éxito", "exito",
    # "EXITO", etc. sean reconocidos como la misma palabra.
    mensaje_normalizado = unicodedata.normalize(
        "NFD",
        mensaje
    ).encode("ascii", "ignore").decode("utf-8").lower()

    # Si el usuario escribe "éxito", "exito", "Éxito", etc.,
    # finalizamos la comunicación.
    if mensaje_normalizado == "exito":

        # Enviamos la palabra de finalización al servidor.
        cliente.sendall(mensaje.encode("utf-8"))

        break

    # Convertimos el mensaje de texto a bytes y
    # lo enviamos al servidor.
    cliente.sendall(mensaje.encode("utf-8"))

    # Esperamos la respuesta enviada por el servidor.
    respuesta = cliente.recv(1024)

    # Convertimos la respuesta recibida de bytes a texto.
    respuesta = respuesta.decode("utf-8")

    # Mostramos la respuesta del servidor.
    print(f"Respuesta del servidor: {respuesta}")

# Cerramos la conexión cuando finaliza la comunicación.
cliente.close()

print("Conexión cerrada.")
