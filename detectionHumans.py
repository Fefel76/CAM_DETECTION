import cv2
import os
import time
import logging
import numpy as np
import imutils
import pandas as pd
import smtplib
#TODO gestion de mails
import pickle
from ComSMS import *

logging.basicConfig(filename='./log/detectionHumans.log',level=logging.DEBUG,format='%(asctime)s -- %(funcName)s -- %(process)d -- %(levelname)s -- %(message)s')


def scanCAM(src=0, name='CAM', width=320, height=240, fps=45, visu="off", record="on", freq_delay=0.3, seuil=5):
    """
    Scrute un flux vidéo pour réaliser une détection , enregistrer et visualiser
    :param src: 0 par défaut pour la webcam sinon adresse rstp://login:mdp@IP
    :param name: Nom de la caméra
    :param width: largeur de l'image => à réduire pour optimiser
    :param height: longueur de l'image
    :param fps: défilement de l'analyse doit être supérieur au FPS de la video
    :param visu: False par défaut, True pour afficher l'image
    :param freq_detect: analyse toutes les images à la fréquence indiquée
    :return: N/A
    """


    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
    logging.info("Début détection sur la caméra: "+name)
    if src != 0:
        cap = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
    else:
        cap= cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.error("Erreur ouverture camera")
        exit()


    print('Images par secondes :', cap.get(cv2.CAP_PROP_FPS) , 'FPS par défaut versus', str(fps),  "FPS configuré")

    width= cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Taille (W,H): ",width,height)

    t=time.time()  # compteur de trames
    parametres = read_param()
    logging.info("Param:"+str(parametres))

    while True:

        """ DECLENCHEMENT  SCAN videos """
        # itération par image capturée
        frame1 = read_frame(cap,name)
        frame2 = read_frame(cap,name)
        frame=frame1.copy()

        """ DECLENCHEMENT  DETECTION """
        # régulation des détections tous les freq_delay
        if time.time()-t>freq_delay:
            record = is_record()  # répérer variable record on/off

            if record == "on":  # Enregistrement de l'image
                parametres = read_param()
                blocs = diff_frame(frame1, frame2,visu=visu, name=name, decoupe=int(parametres['decoupe']),seuil=int(parametres['seuil']))  # Comparaison avec image précédente (nb de bloc différents)
                frame, humains = detectionHOG(frame,ws=int(parametres['winStride']),p=int(parametres['padding']),s=float(parametres['scale']))  # detection HOG
                frame, visages = detection_face_HAAS(frame)  # detection HAAS Face
                t = time.time()

                """ DECLENCHEMENT  ALERTE """
                if (humains+visages)>0 and blocs>seuil: #Détection identifiée
                    print(time.strftime("%d/%m/%y %H:%M:%S"), 'Détections HVB', humains, visages, blocs)
                    photo(frame=frame, name=name)  # sauvegarde sur disque de la photo
                    # Traçage dans un excel l'heure et la date
                    a = pd.DataFrame({"Nom": [name], "ID": [time.time()], "Time": [time.strftime("%d/%m/%y %H:%M:%S")],"Humains": [humains], "Visages": [visages], "Blocs":blocs})
                    a.to_csv('./videos/alertes_'+name+'.csv', mode='a', index=False, header=False, encoding='utf-8')
                    #send_sms("Instrusion "+name+" avec niveau de "+ str(blocs))



        #Affichage de l'image
        if visu=="on":
            cv2.imshow(name, frame)

        if cv2.waitKey(int(1000 / fps)) == ord('q'):
            break
    # Fin de la boucle infinie ==> libération des ressources CV
    cap.release()
    cv2.destroyAllWindows()



def photo(frame,name):
    """
    Stocke la photo dans /videos
    :param frame: image à sauvegarder
    :param name: nom de la caméra
    :return:
    """

    file = "./videos/" + name + "_" + time.strftime("%d-%b-%Y_%HH%Mm%Ss") + '.jpg'
    try:
        cv2.imwrite(file, frame)
        logging.info(name + ": Enregistrement de la photo " + file)
        print(time.strftime("%d/%m/%y %H:%M:%S"),'Photo !')
    except:
        logging.error(name + ': Erreur pour ouvrir le fichier de sauvegarde')



def capture(cap, frame, name, t_capture, d_capture=1, width=640, height=480, fps=15):
    """
    Enregistre le flux vidéo pedant une durée déterminée
    :param cap: flux vidéo à enregistrer
    :param t_capture: début du temps de la vidéo
    :param d_capture: durée de la vidéo à enregistrer
    :return: True/False
    """
    file = "./videos/"+name+"_"+time.strftime("%d-%b-%Y_%HH%Mm%Ss") + '.mp4'

    try:
        writer = cv2.VideoWriter(file, fourcc=cv2.VideoWriter_fourcc(*'DIVX'), fps=fps, frameSize=(int(width), int(height)))
    except:
        logging.error(name + ': Erreur pour ouvrir le fichier de sauvegarde')

    while (time.time()-t_capture<d_capture):
        writer.write(frame)


        # itération par image capturée
        try:
            ret, frame = cap.read()
            if not ret:
                logging.error(name + " : Erreur dans la lecture du stream...")
                break
        except:

            logging.error(name + " : Erreur de récupération du flux")
            break


    logging.info(name + ": Enregistrement de la vidéo " + file)

    try:
        writer.release()
        return True
    except:
        logging.error(name +':Erreur pour fermer le fichier de sauvegarde')
        return False

def detectionHOG(frame, ws=8, p=3, s=1.21):
    """

    :param frame: image à analyser
    :return: image avec les rectangles de détection, nombre d'humains détectés
    """
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     #Optimisation de la détection
    winStride = (ws, ws)
    padding = (p, p)
    scale = s

    (humans, _) = hog.detectMultiScale(gray,winStride=winStride,padding=padding,scale=scale)

    for (x, y, w, h) in humans:
        cv2.rectangle(frame, (x, y),
                      (x + w, y + h),
                      (0, 0, 255), 2)
    return frame, len(humans)

def detection_face_HAAS(frame):
    """

    :param frame: image à analyser
    :return: image avec les rectangles de détection, nb détection
    """
    faceCascade = cv2.CascadeClassifier('./IAModel/haarcascade_frontalface_default.xml')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minNeighbors=10, #5
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return frame, len(faces)

"""
def detection_body_HAAS(frame):
    classifier = cv2.CascadeClassifier('./IAModel/haarcascade_upperbody.xml')
    body = classifier.detectMultiScale(frame, 1.1, 8)
    for (x, y, w, h) in body:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

"""
#TODO gestion multi record
def is_record(record="on"):

    try:
        with open('./conf/record.txt', 'rb') as f:
            record = pickle.load(f)
    except:
        pickle.dump(record, open("./videos/record.txt", "wb"))  # activation record

    return record

def diff_frame(frame1,frame2,decoupe=10, seuil=10, visu="off", name="cam"):
    c=0
    diff = frame1.copy()
    cv2.absdiff(frame1, frame2, diff)

    # converting the difference into grayscale images
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # increasing the size of differences after that we can capture them all
    for i in range(0, 3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i + 1)

    if visu=="on":
        cv2.imshow(name, dilated)
    split= np.array_split(dilated, decoupe, axis=0)

    for i in range(0, decoupe):
        s=np.array_split(split[i],decoupe, axis=1)
        for j in range(0,decoupe):
            if s[j].mean()>seuil:
                c+=1

    return c


def read_frame(cap,name):
    """
    itération par image capturée
    :param cap: flux video
    :param name: nom de la cam
    :return: image capturée
    """

    try:
        ret, frame = cap.read()
        if not ret:
            logging.error(name + " : Erreur dans la lecture du stream..." + ret)


    except:

        logging.error(name + " : Erreur de récupération du flux")


    return frame

def read_param(parametres={"decoupe":10,"seuil":10,"winStride":4,"padding":4,"scale":1.1}):
    """
    lecture des param généraux pour la détection
    :param parametres: dictionnaire pour découpage blocs et classifier HOG
    :return: les paramètres
    """
    try:
        with open('./conf/param.txt', 'rb') as f:
            parametres = pickle.load(f)
    except:
        pickle.dump(parametres, open("./conf/param.txt", "wb"))
        logging.warning("pas de fichier param.txt , création par défaut")

    return parametres


