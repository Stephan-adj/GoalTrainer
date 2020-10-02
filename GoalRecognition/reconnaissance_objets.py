# Ouvrir un terminal et executer la commande ci dessous
# python3 reconnaissance_objets.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# importer tout les packages requis
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import copy
import RPi.GPIO as GPIO


## construction des arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.7, help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

## Initialisation de la liste des objets entrainés par MobileNet SSD 
## création du contour de détection avec une couleur attribuée au hasard pour chaque objet
CLASSES = ["arriere-plan", "avion", "velo", "oiseau", "bateau",
    "bouteille", "autobus", "voiture", "chat", "chaise", "vache", "table",
    "chien", "cheval", "moto", "goal", "plante en pot", "mouton",
    "sofa", "train", "moniteur"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
## Couleur de la boxe du gardien (B,G,R)
COLORS[15]=(0,0,255)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

## chargement des fichiers depuis le répertoire de stockage 
print(" ...chargement du modèle...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

## Initialisation de la caméra du pi, attendre 2s pour la mise au point ,
## Initialisation du compteur FPS
print("...démarrage de la Picamera...")
vs = VideoStream(usePiCamera=True, resolution=(1600, 1200)).start()
time.sleep(5.0)
fps = FPS().start()

## Initialisation des pins du RaspBerry
GPIO.setmode(GPIO.BOARD)     ##je prefere la numerotation BOARD plutot que BCM
#7= 4ème en haut en partant de la droite 

Moteur1A = 16      ## premiere sortie du premier moteur, pin 16
Moteur1B = 18      ## deuxieme sortie de premier moteur, pin 18
Moteur1E = 22      ## enable du premier moteur, pin 22
Moteur2A = 19      ## premiere sortie du deuxième moteur, pin 19
Moteur2B = 21      ## deuxieme sortie de deuxième moteur, pin 21
Moteur2E = 23      ## enable du deuxième moteur, pin 23
capteur1 = 7       ## enable capteur de fin de course 1
capteur2 = 40       ## enable capteur de fin de course 2

GPIO.setup(Moteur1A,GPIO.OUT)    ## ces 6 pins du Raspberry Pi sont des sorties
GPIO.setup(Moteur1B,GPIO.OUT)
GPIO.setup(Moteur1E,GPIO.OUT)
GPIO.setup(Moteur2A,GPIO.OUT)  
GPIO.setup(Moteur2B,GPIO.OUT)
GPIO.setup(Moteur2E,GPIO.OUT)
GPIO.setup(capteur1, GPIO.IN)    ## ces 2 pins du Raspberry Pi sont des entrées
GPIO.setup(capteur2, GPIO.IN)

#Choix du nombre de tir
#NombreDeTir = int(input())
tir = False

## boucle principale du flux vidéo + choix tir + rotation canon
while True :
#while NombreDeTir > 0 :
        #Le temps que le gardien se (re)place avant sa séance de tir
        if tir == True :
            time.sleep(5)
            tir = False
        ## récupération du flux vidéo, redimension 
        ## afin d'afficher au maximum 800 pixels
        frame = vs.read()
        frame = imutils.rotate(frame, angle=180)
        frame = imutils.resize(frame, width=800)

        ## récupération des dimensions et transformation en collection d'images
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        #print("Blob: {}".format(blob.shape))

        ## determiner la détection et la prédiction
        net.setInput(blob)
        detections = net.forward()
    
        ## boucle de détection
        for i in np.arange(0, detections.shape[2]):
                ## calcul de la probabilité de l'objet détecté 
                ## en fonction de la prédiction
                confidence = detections[0, 0, i, 2]
        
                ## supprimer les détections faibles 
                ## inférieures à la probabilité minimale
                if confidence > args["confidence"]:
                        ## extraire l'index du type d'objet détecté
                        ## calcul des coordonnées de la fenêtre de détection 
                        idx = int(detections[0, 0, i, 1])
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")

                        ## creation du contour autour de l'objet détecté
                        ## insertion de la prédiction de l'objet détecté 
                        label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)

                        cv2.rectangle(frame, (startX, startY), (endX, endY), RED, 2)
                        y = startY - 15 if startY - 15 > 15 else startY + 15
                        cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED, 2)
            
                        ###SHOOT
                        #key = cv2.waitKey(1) & 0xFF
                        key = 0
                        #if key == ord("s"):
                        if key == 0 :
                                ##Vérouillage cible
                                cv2.rectangle(frame, (startX, startY), (endX, endY), GREEN, 2)
                                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, GREEN, 2)
                                ## AFFICHAGE
                                cv2.imshow("Frame", frame)
                                #enregistrement de l'image détectée
                                cv2.imwrite("detection.png", frame)                       
                                key = ""
                            
                                ##Coordonnées du shoot
                                #pos = le random qui permet de savoir si on tir à gauche ou à droite du gardien
                                pos = np.random.randint(0, 2)
                                ##print("\n...Le random:...\n")
                                ##print(pos)
                                if pos == 0:
                                    if startX > 45 :
                                        shootX = np.random.randint(25, startX - 20)
                                    else :
                                        shootX = 25
                                else:
                                    if endX >= w - 25 :
                                        shootX = w - 25
                                    elif endX > w - 35 & endX < w - 25 :
                                        shootX = np.random.randint(endX, w - 25)
                                    else :    
                                        shootX = np.random.randint(endX + 10, w - 25)
                                pos2 = np.random.randint(0, 2)        
                                if pos2 == 0:
                                    if startY > 45 :
                                    
                                        shootY = np.random.randint(25, startY - 20)
                                    else :
                                        shootY = 25
                                else:
                                    if endY >= h - 25 :
                                        shootY = h - 25
                                    elif endY < h - 25 & endY > h - 35 :
                                        shootY = np.random.randint(endY, h - 25)
                                    else :    
                                        shootY = np.random.randint(endY + 10, h - 25)
                                print("\n...Coordonnées de la boxe :...\n")
                                print('Selon X : ' + str(startX))
                                print('Selon Y : ' + str(startY))
                                print('Selon X : ' + str(endX))
                                print('Selon Y : ' + str(endY))                              
                                print("\n...Coordonnées du shoot :...\n")
                                print('Selon X : ' + str(shootX))
                                print('Selon Y : ' + str(shootY))
                                shoot = copy.deepcopy(frame)
                                cv2.circle(shoot, (shootX, shootY), 25, RED, 2)
                                cv2.imwrite("Shoot.png", shoot)
                                cv2.imshow("Prévisualisation SHOOT", shoot)
                                cv2.moveWindow("Prévisualisation SHOOT",800, 260)
                                cv2.moveWindow("Frame",0, 260)
                            
                                ##Rotation du canon
                                capteur1 = GPIO.input(7)
                                if capteur1 == GPIO.LOW :
                                    tir = True 
                                    time.sleep(2)
                                    print("Bouton appuyé")
                                    print ("Rotation moteur 1 sens direct, vitesse maximale (rapport cyclique 100%)")
                                    print ("Rotation moteur 2 sens direct, vitesse maximale (rapport cyclique 100%)")
                                    while True :
                                        pwm = GPIO.PWM(Moteur1E,50)   ## pwm de la pin 22 a une frequence de 50 Hz
                                        pwm.start(100)   ## on commemnce avec un rapport cyclique de 100%
                                        pwm2 = GPIO.PWM(Moteur2E,50)   ## pwm de la pin 22 a une frequence de 50 Hz
                                        pwm2.start(100)   ## on commemnce avec un rapport cyclique de 100%
                                        capteur2 = GPIO.input(40)
                                        if capteur2 == GPIO.LOW :
                                            print ("Arret des moteurs")
                                            print ("Canon en place")
                                            GPIO.output(Moteur1E,GPIO.LOW) 
                                            pwm.stop()   
                                            GPIO.output(Moteur2E,GPIO.LOW)
                                            pwm2.stop()    
                                            break                                        
                                        GPIO.output(Moteur1A,GPIO.HIGH)
                                        GPIO.output(Moteur1B,GPIO.LOW)
                                        GPIO.output(Moteur1E,GPIO.HIGH)
                                        GPIO.output(Moteur2A,GPIO.HIGH)
                                        GPIO.output(Moteur2B,GPIO.LOW)
                                        GPIO.output(Moteur2E,GPIO.HIGH)
                                else :
                                    print("nope")
                                    print ("Tir annulé balle pas en place")
            
        # affichage du flux vidéo dans une fenètre
        cv2.imshow("Frame", frame)
    
        # la touche q permet d'interrompre la boucle principale
        key2 = cv2.waitKey(1) & 0xFF
        if key2 == ord("q"):
                break

        # mise à jour du FPS 
        fps.update()
        #prochain tir
        #if tir :
            #NombreDeTir -= 1
#Cleanup des pins
GPIO.cleanup()

# arret du compteur et affichage des informations dans la console
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()