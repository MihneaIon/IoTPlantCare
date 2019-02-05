import RPi.GPIO as GPIO
import dht11
import time
import json
import telepot
import sys

# pini
dth11Pin = 23
gasSensor = 25
channel =21 

# initializare GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(gasSensor, GPIO.IN)


deviceID = 'GasSensor'
# variabila in care voi retine date sun forma de json
dataGaz = {}
dataGaz['id'] = deviceID

deviceHumidityID = 'DTH11_HumiditySensor'
deviceTemperatureID = 'DTH11_TemperatureSensor'

# variabila in care voi retine date sun forma de json
data = {}

instance = dht11.DHT11(pin=dth11Pin)

# campuri destinate senzorului de gaz
gas = GPIO.input(gasSensor)
previousGas = gas

# functie pentru detectarea apei din sol
def detectWater (channel):
    if GPIO.input(channel):
        print("no water detected")
        aux = "no water detected"
        return aux
    else:
        print("water detected")
        aux = "water detected"
        return aux
   
# functie pentru detectarea gazului din mediul limitrof   
def detectGas(gasSensor):
    gas = GPIO.input(gasSensor)
    if gas != previousGas:
        if gas == 0 :
            dataGaz['defaultValue'] = True
            jsonData = json.dumps(data)
            return "gas detected, Warining ! Check your place"
        print(jsonData)
        auxGaz=json.dumps(data)
        time.sleep(0.1)
    return "No gas detected"

        
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300) # sa stim cand valoarea adusa de la pin este mare sau mica
GPIO.add_event_callback(channel,waterDetect) # atribuim funcția pinului GPIO, executam funcția la schimbare

#functie pentru comunicarea dintre raspberrypi si telegram
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    print 'Got command: %s' % command
    
    if command == '/temp':
        bot.sendMessage(chat_id,json.dumps(data))
    elif command == '/water':
        bot.sendMessage(chat_id, detectWater (channel))
    elif command == '/gas':
        bot.sendMessage(chat_id,detectGas(gasSensor))
        
bot = telepot.Bot("Your token access")
bot.message_loop(handle)
print 'I am listening ...'


#fiind un singur fisier com executa try cu except
try:
    while True:
    # variabila result va fi initialziata cu datele provenite de la DHT11 si ne v-a valida informatile din mediul exterior
        result = instance.read()
        if result.is_valid(): # daca result este valid vom retine in variabila data sub forma de json, valoarea adusa si ce anume am primit
            data = {}
            data['id'] = deviceTemperatureID
            data['defaultValue'] = result.temperature
            jsonData = json.dumps(data)
            temp=json.dumps(data)
            print(jsonData)
            time.sleep(1)
            data = {}
            data['id'] = deviceHumidityID
            data['defaultValue'] = result.humidity
            jsonData = json.dumps(data)
            humidityrt = json.dumps(data)
            print(jsonData)
            print(detectGas(gasSensor)) # afisarea rezultatului venit de la functia detectGas
            detectWater (channel) # afisarea rezultatului venit de la functia detectWater
            
            
# caz de tratare a exceptiei in care dorim sa oprim rularea programului
# cu comanda Control + C
except KeyboardInterrupt:
    print('QUIT')
    GPIO.cleanup()
