from datetime import datetime, timedelta

# def turnLightOn(board:serial.Serial) -> None:
#     """
#     Writes to board to turn light on

#     :param board: The board from arduinoDriver
#     """
#     board.write(b'C')

# def turnLightOff(board:serial.Serial) -> None:
#     """
#     Writes to board to turn light off

#     :param board: The board from arduinoDriver
#     """
#     board.write(b'D')

def checkIfLightNeeded(lightStartTime:datetime, isLightOn:bool, timeToKeepLightOn: timedelta, timeToKeepLightOff: timedelta) -> None:
    """
    Checks if the light is needed or not, then turns it
    on or off accordingly.
    """
    now = datetime.now()
    if isLightOn:
        if (lightStartTime + timeToKeepLightOn) >= now:
            # turnLightOn(board)
            return lightStartTime, isLightOn, False
        else:
            # turnLightOff(board)
            return lightStartTime, False, True
    else:
        if (lightStartTime + timeToKeepLightOn + timeToKeepLightOff) <= now:
            # turnLightOn(board)
            return datetime.now(), True, False
        else:
            # turnLightOff(board)
            return lightStartTime, isLightOn, False
        
def calculateLightTimeOn(lightStartTime:datetime) -> int:
    """
    Calculates how many minutes the light has been on in the current interval
    
    :param lightStartTime: The datetime the light was turned on
    """
    try:
        now = datetime.now()
        diff = (now - lightStartTime) # Minute conversion
        # Intervals are every time we store data
        if diff < timedelta(minutes=15): # Started this interval
            return (diff.seconds//60)%60 # How long it's been on
        elif diff < timedelta(hours=8): # Light still on
            return 15 # Time between intervals
        elif diff <= (timedelta(hours=8) + timedelta(minutes=15)): # Ended mid-interval
            return abs(((diff - (timedelta(hours=8) + timedelta(minutes=15))).seconds//60)%60) # It's complicated
        else: # Not on
            return 0
    except Exception as error:
        print('**Error in calculateLightTimeOn: ', error)
        return 0
    