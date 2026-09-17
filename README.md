# TP - Chat Básico Cliente-Servidor con Sockets y SQLite

## Descripción

Este proyecto implementa un chat básico cliente-servidor utilizando Python, sockets TCP/IP y una base de datos SQLite.

El servidor escucha conexiones en `localhost:5000`, recibe mensajes enviados por el cliente, los almacena en una base de datos y devuelve una confirmación con la fecha y hora de recepción.

## Tecnologías utilizadas

* Python
* Sockets TCP/IP
* SQLite
* Módulo `sqlite3`

## Archivos

* `servidor.py`: crea y configura el servidor, recibe los mensajes y los almacena en SQLite.
* `cliente.py`: permite conectarse al servidor y enviar múltiples mensajes.
* `chat.db`: base de datos SQLite generada automáticamente al ejecutar el servidor. No se incluye en el repositorio.

## Base de datos

La tabla `mensajes` contiene los siguientes campos:

* `id`
* `contenido`
* `fecha_envio`
* `ip_cliente`

## Ejecución

Primero se debe ejecutar el servidor:

```bash
python servidor.py
```

Luego, desde otra terminal, ejecutar el cliente:

```bash
python cliente.py
```

El cliente permite enviar múltiples mensajes y muestra la respuesta recibida del servidor.

Para finalizar la comunicación, se debe escribir:

```text
éxito
```

El servidor guarda los mensajes enviados y responde con:

```text
Mensaje recibido: <timestamp>
```
