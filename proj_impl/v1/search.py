 #!/usr/bin/env python
# -*- coding: utf-8 -*-


import MySQLdb as mdb
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as GPIO
import time
import serial
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
s=26
GPIO.setup(s, GPIO.IN)  #
s1=19
GPIO.setup(s1, GPIO.IN)
def push2(var):

        
            con = mdb.connect('localhost', \
                              'root', \
                              'raspberry', \
                              'tms' );
            cur = con.cursor()
            cur.execute("TRUNCATE TABLE `sens`")
            cur.execute("""INSERT INTO sens(status,ss,id) \
                       VALUES(%s,%s,%s)""", (var,var,'1'))
            
            con.commit()
def push4(var):

        
            con = mdb.connect('localhost', \
                              'root', \
                              'raspberry', \
                              'tms' );
            cur = con.cursor()
            cur.execute("TRUNCATE TABLE `sens`")
            cur.execute("""INSERT INTO sens(status,ss,id) \
                       VALUES(%s,%s,%s)""", (var,var,'0'))
            
            con.commit()
def push3():

        
            con = mdb.connect('localhost', \
                              'root', \
                              'raspberry', \
                              'tms' );
            cur = con.cursor()
            cur.execute("TRUNCATE TABLE `sens`")
          
            
            con.commit()             
       


while True:
    if (GPIO.input(s1)):
        try:
            f = PyFingerprint('/dev/ttyAMA0', 9600, 0xFFFFFFFF, 0x00000000)#serial ort define for gpio serial ttyAM0 and 9600 is baud rate

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)


        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))


        try:
            print('Waiting for finger...')

           
            while ( f.readImage() == False ):
                pass

           
            f.convertImage(0x01)

           
            result = f.searchTemplate()
            positionNumber = result[0]

            if ( positionNumber >= 0 ):
                print('Template already exists at position #' + str(positionNumber))
                exit(0)

            print('Remove finger...')
            time.sleep(2)

            print('Waiting for same finger again...')

            while ( f.readImage() == False ):
                pass



            f.convertImage(0x02)

          
            if ( f.compareCharacteristics() == 0 ):
                raise Exception('Fingers do not match')

            
            f.createTemplate()

           
            positionNumber = f.storeTemplate()
            print('Finger enrolled successfully!')
            print('New template position #' + str(positionNumber))
            var=str(('New template position #' + str(positionNumber)))
            push2(var)
            
            
        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)
    if (GPIO.input(s)):
        print "person detected"
        try:
            f = PyFingerprint('/dev/ttyAMA0', 9600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)


        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))


        try:
            print('Waiting for finger...')

           
            while ( f.readImage() == False ):
                pass


            f.convertImage(0x01)

            
            result = f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            if ( positionNumber == -1 ):
                print('No match found!')
                var="No match found!"
                push4(var)
                exit(0)
            else:
                var=str('Found template at position #' + str(positionNumber))
                print var
                push2(var)
                time.sleep(4)
                push3()
                print('The accuracy score is: ' + str(accuracyScore))

          
            f.loadTemplate(positionNumber, 0x01)

          
            characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')


            print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)
