# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from detectionHumans import *
import configparser
import ast

def init_config():
    config=configparser.ConfigParser()
    url = 0  # par défaut , canal 0 de la webcam
    name = 'CAM'
    visu = False
    record = True
    fps = 45
    file="cam.conf"
    lire = open(file, 'r')
    contenu = lire.read()
    d = ast.literal_eval(contenu) # conversion en dictionnaire

    if len(sys.argv) > 1:    # récup de l'argument pour selectionner la caméra (config du fichier)
        name = sys.argv[1]
        url = d[name]
        print(name,url)

    return url, name, visu, fps, record



    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    src, name, visu, fps, record= init_config()

    scanCAM(src=src, name=name, visu=visu, fps=fps, record=record)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
