# Third Party
from datetime import datetime
import serial
import time

# Proprietary
from controllers.sendEmail import notifyLowWater, notifyWaterFilled
from controllers.sendData import checkIfDataNeedsSent
from controllers.signalArduino import determineSignalToSend
from controllers.waterPump import checkIfPumpNeeded
from controllers.lightValue import checkIfLightNeeded
from controllers.dataArray import DataArray


board = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = None,
)

# Data comes in as temperature,humidity,moisture,timeLightOn,floatSensor
temp = 70
hum = 20
moisture = 0

timeToKeepLightOn = 28800
timeToKeepLightOff = 57600
lightStartOn = 0
timeLightOn = 0
isLightOn = False
lightBool = True
lightOn = False
# lightArray = DataArray(101, 20)

timeToKeepPumpOn = 0
timeToKeepPumpOff = 0
pumpStartOn = 0
timePumpOn = 0
isPumpOn = False
pumpBool = True

floatFlag = 'LOW'
emailSent = False
emailTimestamp = 0

moistureHigh = 450
moistureArray = DataArray(moistureHigh, 5)

timeDataCollected = 0
lastMinuteSent = 1
envId = 1
signalSentBool = False

def checkIfEmailNeeded(floatFlag, emailTimestamp):
    global emailSent
    currentTime = time.time()
    if(currentTime - emailTimestamp > 86400):#86400 seconds in 24 hours
        emailSent = False
    if(floatFlag == 'LOW' and not emailSent):
        notifyLowWater(currentTime)
        emailSent = True
        emailTimestamp = time.time()
    if(floatFlag == 'HIGH' and emailSent):
        notifyWaterFilled(currentTime)
        emailSent = False
    return emailTimestamp

while True:
    try:
        while(board.inWaiting() == 0):
            if temp != 0 and moisture != 0:
                emailTimestamp = checkIfEmailNeeded(floatFlag, emailTimestamp)
                if pumpBool:
                    pumpStartOn, isPumpOn, endTime = checkIfPumpNeeded(floatFlag, pumpStartOn, isPumpOn, timeToKeepPumpOn, timeToKeepPumpOff)
                    if endTime:
                        timePumpOn += int((datetime.now() - pumpStartOn).total_seconds()/60)
                    pumpBool = False
                if temp != -999:
                    returned = checkIfDataNeedsSent(lastMinuteSent, temp, hum, moistureArray.getAvg(), timeLightOn, timePumpOn, timeDataCollected, envId)
                    if returned != lastMinuteSent:
                        lastMinuteSent = returned
                        timeLightOn = 0
                        timePumpOn = 0
                if lightBool:
                    lightStartOn, isLightOn, endTime = checkIfLightNeeded(lightStartOn, isLightOn, timeToKeepLightOn, timeToKeepLightOff)
                    if endTime:
                        timeLightOn += int((datetime.now() - lightStartOn).total_seconds()/60)
                    lightBool = False
                if not signalSentBool:
                    determineSignalToSend(isPumpOn, isLightOn, board)
                    signalSentBool = True
        timeDataCollected = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        output = board.readline().decode('utf-8').strip().split(',')
        if len(output) == 6:
            # temp = output[0]
            # hum = output[1]
            moisture = int (output[2])
            moistureArray.add(moisture)
            # lightArray.add(output[3])
            if 'LOW' in output[4]:
                floatFlag = 'LOW'
            else:
                floatFlag = 'HIGH'
            pumpBool = True
            lightBool = True
            signalSentBool = False
            print(output)
        else:
            print("Incomplete board output: ", output)
            continue
    except Exception as error:
        print('**Error reading board: ', error)
