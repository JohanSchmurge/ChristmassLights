import network, time
import time
from config import SSID, AP, STA


network.WLAN(network.AP_IF).active(AP)
wlan = network.WLAN(network.STA_IF)
wlan.active(STA)


def start():
    if wlan.isconnected():
        print('Wi-Fi already connected.')
    else:
        t0 = time.time()+20
        wlan.connect(SSID[0], SSID[1])
        while not wlan.isconnected():
            time.sleep_ms(500)
            if t0 < time.time():
                print('Wi-fi connection timeout')
                break
    print(wlan.ifconfig())


def stop():
    wlan.disconnect()


def status():
    if wlan.isconnected(): return True
    else:
        debug('Wlan disconnected.')
        return False
