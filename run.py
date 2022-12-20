import sys
import os
from detectionHumans import *
import configparser
import ast
import pickle

def init_config():
    config=configparser.ConfigParser()
    url = 0  # par défaut , canal 0 de la webcam
    name = 'CAM'
    visu = "off"
    record = "on"
    fps = 45
    file="cam.conf"
    lire = open(file, 'r')
    contenu = lire.read()
    d = ast.literal_eval(contenu) # conversion en dictionnaire

    # Récupération des variable d'environnements
    visu= os.environ.get('CAM_VISU', visu)
    record = os.environ.get('CAM_RECORD', record)

    login = os.environ.get('CAM_LOGIN', "no_log")
    pwd= os.environ.get('CAM_PWD',"no_pass")
    print("RECORD", record)
    print("VISU", visu)

    if len(sys.argv) > 1:    # récup de l'argument pour selectionner la caméra (config du fichier)
        name = sys.argv[1]
        url = d[name]
        url='rtsp://'+login+':'+pwd+'@'+url

    return url, name, visu, fps, record

    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #TODO utilisation de click pour gérer les arguments et options
    src, name, visu, fps, record= init_config()
    #TODO gestion multi record
    pickle.dump(record, open("./videos/record.txt", "wb"))  # activation record
    scanCAM(src=src, name=name, visu=visu, fps=fps, record=record)




