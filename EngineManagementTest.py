import RPi.GPIO as GPIO
import cv2
import time

GPIO.setwarnings(False)

Moteur1A = 16      ## premiere sortie du premier moteur, pin 16
Moteur1B = 18      ## deuxieme sortie de premier moteur, pin 18
Moteur1E = 22      ## enable du premier moteur, pin 22
Moteur2A = 19      ## premiere sortie du deuxième moteur, pin 19
Moteur2B = 21      ## deuxieme sortie de deuxième moteur, pin 21
Moteur2E = 23      ## enable du deuxième moteur, pin 23
capteur1 = 7       ## enable capteur de fin de course 1



while True:
    GPIO.setmode(GPIO.BOARD)     ##je prefere la numerotation BOARD plutot que BCM  
    GPIO.setup(Moteur1A,GPIO.OUT)  ## ces 6 pins du Raspberry Pi sont des sorties
    GPIO.setup(Moteur1B,GPIO.OUT)
    GPIO.setup(Moteur1E,GPIO.OUT)
    GPIO.setup(Moteur2A,GPIO.OUT)  
    GPIO.setup(Moteur2B,GPIO.OUT)
    GPIO.setup(Moteur2E,GPIO.OUT)
    GPIO.setup(capteur1, GPIO.IN) 
    state = GPIO.input(7)
    if state == GPIO.LOW :
        durée = 15
        pwm = GPIO.PWM(Moteur1E,50)   ## pwm de la pin 22 a une frequence de 50 Hz
        pwm.start(100)   ## on commemnce avec un rapport cyclique de 100%
        pwm2 = GPIO.PWM(Moteur2E,50)   ## pwm de la pin 22 a une frequence de 50 Hz
        pwm2.start(100)   ## on commemnce avec un rapport cyclique de 100%
        print("Bouton appuyé")
        print ("Rotation moteur 1 sens direct, vitesse maximale (rapport cyclique 100%)")
        GPIO.output(Moteur1A,GPIO.HIGH)
        GPIO.output(Moteur1B,GPIO.LOW)
        GPIO.output(Moteur1E,GPIO.HIGH)
        print ("Rotation moteur 2 sens direct, vitesse maximale (rapport cyclique 100%)")
        GPIO.output(Moteur2A,GPIO.HIGH)
        GPIO.output(Moteur2B,GPIO.LOW)
        GPIO.output(Moteur2E,GPIO.HIGH)
        time.sleep(durée)
        GPIO.output(Moteur1E,GPIO.LOW)
        pwm.stop()    ## interruption du pwm
        GPIO.output(Moteur2E,GPIO.LOW)
        pwm2.stop()    ## interruption du pwm
        print ("Arret du moteur")
        #Cleanup des pins
        GPIO.cleanup()
    else :
        print("nope")
    time.sleep(1)    
    key = cv2.waitKey(2) & 0xFF
    if key == ord("s"):
        break    
