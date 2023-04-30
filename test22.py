import cv2
import os

# Establecer el tiempo de grabación en segundos
tiempo_grabacion = 10

# Establecer la fuente de captura como la cámara predeterminada
captura = cv2.VideoCapture(0)

# Establecer el codec y crear el objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Obtener la ruta de la carpeta "captura" en el escritorio
ruta_carpeta = os.path.join(os.path.expanduser("~"), "Desktop", "captura")

# Crear la carpeta si no existe
if not os.path.exists(ruta_carpeta):
    os.makedirs(ruta_carpeta)

# Establecer la ruta completa del archivo de video a guardar
ruta_guardado = os.path.join(ruta_carpeta, "video_capturado.mp4")
guardado = cv2.VideoWriter(ruta_guardado, fourcc, 30, (640,480))

# Iniciar la grabación
while(captura.isOpened() and tiempo_grabacion > 0):
    ret, frame = captura.read()
    if ret==True:
        # Escribir el frame en el objeto VideoWriter
        guardado.write(frame)
        
        # Reducir el tiempo de grabación en un segundo
        tiempo_grabacion -= 1
    else:
        break

# Liberar los recursos
captura.release()
guardado.release()

# Imprimir la ruta de la ubicación de almacenamiento
print("Video guardado en la ubicación: ", ruta_guardado)
