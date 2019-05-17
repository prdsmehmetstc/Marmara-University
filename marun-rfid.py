# Mehmet SUTCU - 2019
# info@mehmetsutcu.com
# Raspberry Pi 3 ile Ag Destekli RFID Kartli Gecis Sistemi
from pirc522 import RFID
import signal
import time
import RPi.GPIO as GPIO 
import paho.mqtt.client as mqtt
istemci = mqtt.Client()

def mesaj_geldiginde(client, userdata, msg):
 print msg.topic+" "+str(msg.payload)

def baglanti_saglandiginda(client, userdata, flags, rc):
 print "Raspberry Pi sunucuya baglandi!"
 istemci.subscribe("/marun/rfid")
 istemci.publish("/marun/rfid", "Sistem hazir!")

def baglanti_kesildiginde(client, userdata, rc):
 istemci.connect("iot.eclipse.org", 1883, 5)

istemci.on_connect = baglanti_saglandiginda
istemci.on_message = mesaj_geldiginde
istemci.on_disconnect = baglanti_kesildiginde
istemci.connect("iot.eclipse.org", 1883, 5)

print "Marmara Universitesi Teknik Bilimler MYO"
print "Raspberry Pi RFID Kartli Gecis Kontrol Sistemi"
print "Ctrl+C tus kombinasyonu ile programi durdurabilirsiniz."
relayPin = 7
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relayPin, GPIO.OUT)
rdr = RFID()
util = rdr.util()
util.debug = True

while True:
	rdr.wait_for_tag()
	(error, data) = rdr.request()
	if not error:
		print("\nKart Algilandi!")
		istemci.publish("/marun/rfid", "Kart algilandi!")
		(error, uid) = rdr.anticoll()
		if not error:
			
			kart_uid = str(uid[0])+" "+str(uid[1])+" "+str(uid[2])+" "+str(uid[3])+" "+str(uid[4])
			print(kart_uid)
			istemci.publish("/marun/rfid", kart_uid)
			if kart_uid == "112 253 138 166 161":
				print("Hos Geldiniz, Kart Sahibi.")
				istemci.publish("/marun/rfid", "Kart Sahibi kapiyi acti!")
				GPIO.output(relayPin, GPIO.LOW)
				time.sleep(3)
				GPIO.output(relayPin, GPIO.HIGH)
			else: 
				print("HATA! Yetkisiz Kart!")
				istemci.publish("/marun/rfid", "Okunan kart yetkisiz!")
				GPIO.output(relayPin, GPIO.HIGH)
				time.sleep(2)

istemci.loop_forever()

