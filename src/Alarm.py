import winsound
import time

def alarm():
    winsound.Beep(600, 250)
    time.sleep(0.25)
    winsound.Beep(750, 250)

def checkalarmStatus(percentageValue, threshold, i, window):
    if abs(percentageValue) > abs(threshold):
        alarm()
        window['Difference ' + str(i)].update(background_color='blue')
