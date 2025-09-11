"""
Script para la deteción y dibuj de contornos
"""

import numpy as np
import cv2 as cv


"""
Abrir imagen
"""

im = cv.imread('20230420_134658.jpg')
assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


"""
Detectar contornos
"""



"""
Dibujar contornos
"""

# cv.drawContours(im, contours, -1, (0,255,0), 3)
#
# # Mostrar la imagen con los contornos detectados
# cv.imshow('Contornos Detectados', im)
# cv.waitKey(0)
# cv.destroyAllWindows()

if len(contours) >= 2:
    # Ordenar los contornos por área, de mayor a menor
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # Dibujar el segundo mayor contorno
    segundo_mayor_contorno = contours[1]  # Segundo mayor
    # cv.drawContours(im, [segundo_mayor_contorno], -1, (0, 255, 0), 3)

    # Crear una máscara con el mismo tamaño que la imagen, inicialmente negra
    mascara = np.zeros_like(im)

    # Dibujar el segundo mayor contorno en la máscara, llenándolo (blanco en el área del contorno)
    cv.drawContours(mascara, [segundo_mayor_contorno], -1, (255, 255, 255), thickness=cv.FILLED)

    # Aplicar la máscara a la imagen original
    imagen_recortada = cv.bitwise_and(im, mascara)

    # Mostrar la imagen con solo el área dentro del segundo mayor contorno
    cv.imshow('Imagen Recortada', imagen_recortada)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print("No hay suficientes contornos rectangulares detectados.")

"""
Aislar contorno deseado y convertir superficie de probeta en 100%
"""



# import cv2
# import numpy as np
#
# # Cargar la imagen
# imagen = cv2.imread('20230420_134658.jpg')
# # Convertir a escala de grises
# gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
#
# # Aplicar desenfoque para reducir ruido
# blur = cv2.GaussianBlur(gris, (5, 5), 0)
#
# # Aplicar detección de bordes (Canny)
# bordes = cv2.Canny(blur, 50, 150)
#
# # Encontrar contornos
# contornos, _ = cv2.findContours(bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
# # Filtrar y dibujar contornos rectangulares
# for contorno in contornos:
#     # Aproximar el contorno a un polígono
#     perimetro = cv2.arcLength(contorno, True)
#     aproximacion = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)
#
#     # Si el polígono tiene 4 lados, es decir, es un rectángulo
#     if len(aproximacion) == 4:
#         # Obtener el bounding box (cuadro que encierra el contorno)
#         x, y, w, h = cv2.boundingRect(aproximacion)
#
#         cv2.drawContours(imagen, [aproximacion], -1, (0, 255, 0), 3)
#
# # Mostrar la imagen con los contornos detectados
# cv2.imshow('Contornos Detectados', imagen)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
