from PIL import Image
import numpy as np
import os
import pytesseract
import matplotlib.pyplot as plt
import cv2
from re import sub


os.chdir("images")

imagenes = !ls *.png



def get_cut_coor(np_img):
    left = 0
    top  = 150
    bandera_inicio = False
    while bandera_inicio is False:
        for i in range(np_img.shape[1]):
            if all(np_img[top,i]==verde) and left==0:
                bandera_inicio = True
                left = i
                #print("indice [{},{}]".format(top,left))
        top +=1

    top = top + 87
    bottom = top
    right  = 0
    bandera_final = False

    while bandera_final is False:
        for i in range(np_img.shape[1]):
            if all(np_img[bottom,i]==verde):
                bandera_final = True
                right = i
                #print("indice [{},{}]".format(bottom,right))
        bottom +=1

        if bottom==np_img.shape[0]:
            bandera_final= True
            right = 1501
            bottom = 1158
    return left,top,right,bottom


## Definimos el color rgb del verde
verde = [ 49, 185, 146]

## Recortamos la imagen para cada ZM
for imagen in imagenes:
    print(imagen)
    # Abrimos la imagen en modo RGB
    im = Image.open(imagen)

    # Convertimos la imagen en array
    np_img = np.array(im)

    # Obtenemos las posiciones para realizar el corte
    coordenadas = get_cut_coor(np_img)

    # Recortamos la imagen con las dimensión definida
    im1 = im.crop(coordenadas)

    # Guardamos la imagen
    image_name = imagen[:-3]+"pdf"
    im1 = im1.convert('RGB')
    #im1= im1.convert('RGB')
    im1.save(imagen)
    print(coordenadas)
    #print(pytesseract.image_to_string(im1, config='--psm 6'))

f = open("resultados.txt", "w")
f.close()

for imagen in imagenes:

    img = cv2.imread(imagen)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (0, 0, 100), (255, 5, 255))
    #cv2.imshow('mask before and with nzmask', mask);

    # Build mask of non black pixels.
    nzmask = cv2.inRange(hsv, (0, 0, 5), (255, 255, 255))

    # Erode the mask - all pixels around a black pixels should not be masked.
    nzmask = cv2.erode(nzmask, np.ones((3,3)))
    #cv2.imshow('nzmask', nzmask);

    mask = mask & nzmask

    new_img = img.copy()
    new_img[np.where(mask)] = 255

    #cv2.imshow('mask', mask);
    #cv2.imshow('new_img', new_img);
    texto = pytesseract.image_to_string(new_img, config='--psm 6')
    nombre_file = imagen[:-4]
    texto = texto.replace("\n"," "+sub(pattern=r"\d", repl=r"", string=nombre_file) +"\n")
    texto = texto.replace("— ","")
    texto = texto.replace("=","")
    texto = texto.replace("—_","")
    texto = texto.replace(". "," ")

    print(texto)
    f = open('resultados.txt', 'a')
    f.write(texto)
    f.close()



# https://stackoverflow.com/questions/61223862/how-to-remove-background-gray-drawings-from-image-in-opencv-python
# https://nanonets.com/blog/ocr-with-tesseract/
# https://www.opcito.com/blogs/extracting-text-from-images-with-tesseract-ocr-opencv-and-python
# 
