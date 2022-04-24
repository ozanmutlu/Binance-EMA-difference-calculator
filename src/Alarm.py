import winsound
import time
from datetime import datetime

def alarm():
    winsound.Beep(600, 250)
    time.sleep(0.25)
    winsound.Beep(750, 250)

def checkalarmStatus(percentageValue, threshold, i, window):
    now = datetime.now()
    current_time = now.strftime("%M")

    if abs(percentageValue) > abs(threshold) and int(current_time) % 15 > 12:
        alarm()
        window['Difference ' + str(i)].update(background_color='blue')
