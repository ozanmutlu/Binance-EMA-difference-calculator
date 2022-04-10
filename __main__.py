import sys

from numpy import size
sys.path.append('src/.')

from multiprocessing import Value
import time
from src.EmaValue import getEMA
from src.Current_Value import currentValue
import PySimpleGUI as sg
from src.Alarm import checkalarmStatus
from src.timeFrameHandler import timeFrameFunc
from src.saveLoad import loadFunc, saveFunc

rangeNumber = 10
use_custom_titlebar = True

def callEMA(coin):
    for key, value in values.items():
        if str(value) == 'True' and str(key).startswith('Radio'):
            timeFrame = timeFrameFunc(key)

    timePeriod = int(values['TimePeriod'])
    
    EMA_Value, timeValueEMA = getEMA(coin, str(timeFrame), int(timePeriod), values['Algorithm'])
    return EMA_Value, timeValueEMA

def getCurrentValue(coin):
    currentValueOfCoin = currentValue(coin.replace("/", ""))
    return currentValueOfCoin

def CalculatePercentage(i, coin):
    EMA_Value, timeValueEMA = callEMA(coin)
    currentValueOfCoin = getCurrentValue(coin)

    PercentageValue = format((((float(currentValueOfCoin) - float(EMA_Value)) / float(EMA_Value)) * 100), ".2f")
    window['Difference ' + str(i)].update(PercentageValue + '%', background_color=sg.theme_background_color())
    window['EMA ' + str(i)].update(format(float(EMA_Value), ".4f"))
    window['Fiyat ' + str(i)].update(currentValueOfCoin)
    if values['Alarm_on'] and values['AlarmThreshold']:
        checkalarmStatus(float(PercentageValue), float(values['AlarmThreshold']), i, window)
    window.refresh
    time.sleep(0.5)

def make_window(theme='DarkAmber'):

    NAME_SIZE = 23

    sg.theme(theme)


    layout_top = [  [sg.Text('', size=(NAME_SIZE,1), justification='center',pad=(0,0), font='_ 12')],
                    [sg.Combo(list(['Ta-lib', 'Pandas']), enable_events=False, key='Algorithm', font='_ 10', default_value='Ta-lib', readonly=True),
                    sg.Text('Zaman Aralığı', size=(NAME_SIZE,1), justification='center',pad=(0,0), font='_ 12'), 
                        sg.Radio('1dk', 1 , key='Radio_1'), sg.Radio('5dk', 1 , key='Radio_2'), sg.Radio('15dk', 1 , key='Radio_3', default=True), sg.Radio('30dk', 1 , key='Radio_4'), 
                        sg.Radio('1s', 1 , key='Radio_5'), sg.Radio('2s', 1 , key='Radio_6'), sg.Radio('4s', 1 , key='Radio_7'), sg.Radio('6s', 1 , key='Radio_8'),
                        sg.Radio('12s', 1 , key='Radio_9'), sg.Radio('1g', 1 , key='Radio_10'), sg.Radio('1h', 1 , key='Radio_11')],
                    [sg.Text('Zaman Periyodu(MA)', size=(NAME_SIZE,1), justification='center',pad=(0,0), font='_ 12'),
                        sg.Slider((2,99), orientation='h', s=(70,30), key='TimePeriod', default_value=7)]]

    layout_l = []
    layout_l.append([sg.T('Coin İsmi', font='_ 15', justification='c', expand_x=True)])

    for i in range(rangeNumber):
        layout_l.append([sg.Input(s=15, key='Form ' + str(i), size=(25,1))])
    layout_l.append([sg.Button('Kaydet', enable_events=True, size=(6,1), expand_x=True, focus=True), sg.Button('Yükle', enable_events=True, size=(6,1), expand_x=True)])

    layout_l2  = []
    layout_l2.append([sg.T('EMA', font='_ 15', justification='c', expand_x=True)])
    for i in range(rangeNumber):
        layout_l2.append([sg.Text('---', key='EMA ' + str(i), size=(25,1), justification='c')])
    layout_l2.append([sg.Text('')])
    
    layout_r  = []
    layout_r.append([sg.T('Fark', font='_ 15', justification='c', expand_x=True)])
    for i in range(rangeNumber):
        layout_r.append([sg.Text('---', key='Difference ' + str(i), size=(25,1), justification='c', expand_x=True)])
    layout_r.append(
        [sg.Text('Alarm',pad=(5,0), font='_ 12'), sg.Input(key='AlarmThreshold', size=(5,1), default_text='0.02'), sg.Text('%'),
        sg.Radio('Açık', 2 , key='Alarm_on', expand_x=True), sg.Radio('Kapalı', 2 , key='Alarm_off', default=True, expand_x=True)]
    )

    layout_r2  = []
    layout_r2.append([sg.T('Fiyat', font='_ 15', justification='c', expand_x=True)])
    for i in range(rangeNumber):
        layout_r2.append([sg.Text('---', key='Fiyat ' + str(i), size=(25,1), justification='c')])
    layout_r2.append([sg.Text('')])

    layout_c = [[sg.Button('Başla', size=(6,1)), sg.Button('Çıkış', size=(6,1))]]

    layout = [  [sg.Col(layout_top, element_justification='center')],
                [sg.Column(layout_l), sg.Column(layout_l2), sg.Column(layout_r2), sg.Col(layout_r,justification='c')],
                [sg.Column(layout_c ,justification='center')]]
    
    timeout = thread = None

    window = sg.Window('Coin EMA', layout, finalize=True, keep_on_top=True, use_custom_titlebar=use_custom_titlebar, element_justification='center')           

    return window


window = make_window()

while True:
    sg.set_options(suppress_raise_key_errors=True, suppress_error_popups=True, suppress_key_guessing=True)
    event, values = window.read(timeout=1)
    window.refresh()
    if event == sg.WIN_CLOSED or event == 'Çıkış':
        break
    elif event == 'Kaydet':
        saveFunc(values)
    elif event == 'Yükle':
        loadFunc(window)
    elif event == 'Başla':
        for i in range(rangeNumber):
            if values['Form ' + str(i)] and event == 'Başla':
                coin = values['Form ' + str(i)]
                window.read(timeout=1000)
                window.perform_long_operation(lambda : CalculatePercentage(i, coin), 'Başla')
        event, values = window.read(timeout=1)

window.close()