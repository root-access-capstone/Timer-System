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

    :param avg: The average value of the LightArray
    :param lightTurnedOn: Timestamp when the light was turned on
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