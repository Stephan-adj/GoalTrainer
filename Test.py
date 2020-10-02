import RPi.GPIO as GPIO
import cv2
import time

GPIO.setmode(GPIO.BOARD)     ##je prefere la numerotation BOARD plutot que BCM
#7= 4ème en haut en partant de la droite 

Moteur1A = 16      ## premiere sortie du premier moteur, pin 16
Moteur1B = 18      ## deuxieme sortie de premier moteur, pin 18
Moteur1E = 22      ## enable du premier moteur, pin 22
capteur1 = 7

GPIO.setup(Moteur1A,GPIO.OUT)  ## ces trois pins du Raspberry Pi sont des sorties
GPIO.setup(Moteur1B,GPIO.OUT)
GPIO.setup(Moteur1E,GPIO.OUT)
GPIO.setup(capteur1, GPIO.IN)         ## ces trois pins du Raspberry Pi sont des entrées

pwm = GPIO.PWM(Moteur1E,50)   ## pwm de la pin 22 a une frequence de 50 Hz

while True:
    state = GPIO.input(7)
    if state == GPIO.LOW :
        pwm.start(100)   ## on commemnce avec un rapport cyclique de 100%
        print("Bouton appuyé")
        print ("Rotation sens direct, vitesse maximale (rapport cyclique 100%)")
        GPIO.output(Moteur1A,GPIO.HIGH)
        GPIO.output(Moteur1B,GPIO.LOW)
        GPIO.output(Moteur1E,GPIO.HIGH)
        time.sleep(1)
    else :
        print("nope")
        print ("Moteur à l'arret")
        GPIO.output(Moteur1E,GPIO.LOW)
        pwm.stop()    ## interruption du pwm
        time.sleep(1)    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        break    

print ("Arret du moteur")
GPIO.output(Moteur1E,GPIO.LOW)

pwm.stop()    ## interruption du pwm

GPIO.cleanup()
