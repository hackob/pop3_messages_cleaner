# POP3 Message Cleaner

El objetivo de este pequeño código es porder realziar en forma batch (fuera de línea) una depuración de un buzón POP3. Esto para mi fue necesario ya que uno de mis clientes se negó a modificar la configuración por defecto de su cliente de correo y dejeba toda copia de correo en el servidor y también se negó a crecer el almacenamiento.

Con esto en mente el programa depura todo mensaje que tenga más de 180 días y el resto lo deja. Cada mensaje a ser borrado es escrito en un archivo bajo la ruta bkp_messages por si se da el caso de que quieras recuperarlo.

## ¿Qué se requiere?

El único requisito, si quieres puedes modificar esto por tu cuenta, es que el bozón deba se accedido por SSL.

## Configuración

El programa requiere de un archivos de configuración config.py, incluyo un archivo de ejemplo. Desde este archivo se configura lo siguiente:

```python
POP_SERVER='pop3.mydomain.com'      # Dirección IP del servifor POP3
POP_SERVER_PORT='995'               # Puerto en el que escucha el POP3, normalmente no es necesario modificar esto

POP_USER='iam@mydomain.com'         # Usuario con el que te conectas a tu cuenta
POP_PASSWD='My_Super_Password_'     # Tu contraseña

DAYS_TO_MARK_OLD = 180              # El número de días que quieres dejar en el buzón
```
