import uasyncio
import time
import wifi
import config
from machine import Pin, PWM
from random import getrandbits


r1 = PWM(Pin(4), freq=500)
g1 = PWM(Pin(5), freq=500)
b1 = PWM(Pin(12), freq=500)
r2 = PWM(Pin(13), freq=500)
g2 = PWM(Pin(14), freq=500)
b2 = PWM(Pin(15), freq=500)
CH1, CH2 = (r1, g1, b1), (r2 ,g2, b2)


async def blink(led, duty=1000, period_on=500, period_off=500, cycles=1):
    while cycles:
        led.duty(duty)
        await uasyncio.sleep_ms(period_on)
        led.duty(0)
        await uasyncio.sleep_ms(period_off)
        cycles -= 1


async def fade(led, duty=1024, delay=1):
    step = duty // 64
    for i in range(64):
        await uasyncio.sleep_ms(delay)
        led.duty(i * step)
    for i in range(63, -1, -1):
        await uasyncio.sleep_ms(delay)
        led.duty(i * step)


async def fade_up(led, duty=1000, delay=1):
    step = duty // 64
    for i in range(64):
        await uasyncio.sleep_ms(delay)
        led.duty(i * step)


async def fade_down(led, duty=1000, delay=1):
    step = duty // 64
    for i in range(63, -1, -1):
        await uasyncio.sleep_ms(delay)
        led.duty(i * step)


async def flame(led1, led2=None, cycles=200):
    while cycles:
        d = getrandbits(10)
        await uasyncio.sleep_ms(100)
        led1.duty(d)
        if led2:
            led2.duty(int(d * 0.4))
        cycles -=1


def disable_all():
    for led in CH1: led.duty(0)
    for led in CH2: led.duty(0)

def set_color(rgbw=None, num=None):
    # Tuple of colors: RED, GREEN, BLUE, WHITE, ORANGE, YELLOW, CYAN, VIOLET,
    # PINK, CRIMSON, PURPLE, CRIOLA, SAPPHIRE, GR_BLUE, FUXIA, LEMON
    colors = ((1024, 0, 0), (0, 1024, 0), (0, 0, 1024), (1024, 1024, 1024), \
        (1024, 400, 0), (1024, 600, 0), (0, 1024, 1024), (1024, 0, 200) , \
        (1024, 400, 400), (1024, 0, 50), (1024, 0, 700), (1024, 400, 100), \
        (100, 400, 1024), (0, 1024, 100), (1024, 0, 1024), (1024, 1000, 400))
    if num:
        return colors[num]
    if rgbw: color = colors[getrandbits(2)]
    else: color = colors[getrandbits(4)]
    return color


def set_color1():
    color = getrandbits(2)
    if color == 3: color = 0
    return color


def set_delay(delay=5):
    delay = getrandbits(delay)
    if delay == 0: delay = 1
    return delay


def prog_1():
    print('prog_1 started')
    for i in range(10):
        color = set_color()
        for j in range(3):
            uasyncio.create_task(blink(CH1[j], duty=color[j]))
        color = set_color()
        for j in range(3):
            uasyncio.create_task(blink(CH2[j], duty=color[j]))
        await uasyncio.sleep_ms(1000)
        for j in range(3):
            uasyncio.create_task(blink(CH1[j], duty=color[j]))
        color = set_color()
        for j in range(3):
            uasyncio.create_task(blink(CH2[j], duty=color[j]))
        await uasyncio.sleep_ms(1000)
        for j in range(3):
            uasyncio.create_task(blink(CH1[j], duty=color[j]))
        color = set_color()
        for j in range(3):
            uasyncio.create_task(blink(CH2[j], duty=color[j]))
        await uasyncio.sleep_ms(2000)
        disable_all()

def prog_2():
    print('prog_2 started')
    for i in range(10):
        for j in range(3):
            color = set_color()
            for k in range(3):
                uasyncio.create_task(blink(CH1[k], duty=color[k]))
            await uasyncio.sleep_ms(500)
            color = set_color()
            for k in range(3):
                uasyncio.create_task(blink(CH2[k], duty=color[k]))
            await uasyncio.sleep_ms(500)
        disable_all()


def prog_3():
    print('prog_3 started')
    dly= set_delay(6)
    for i in range(20):
        for i in range(3):
            color = set_color()
            uasyncio.create_task(fade(CH1[i], duty=color[i], delay=dly))
            await uasyncio.sleep_ms(64 * dly)
        for i in range(3):
            color = set_color()
            uasyncio.create_task(fade(CH2[i], duty=color[i], delay=dly))
            await uasyncio.sleep_ms(64 * dly)
        disable_all()


def prog_4():
    print('prog_4 started')
    dly= set_delay(6)
    for i in range(20):
        color = set_color()
        for i in range(3):
            uasyncio.create_task(fade(CH1[i], duty=color[i], delay=dly))
        await uasyncio.sleep_ms(128 * dly + 500)
        color = set_color()
        for i in range(3):
            uasyncio.create_task(fade(CH2[i], duty=color[i], delay=dly))
        await uasyncio.sleep_ms(128 * dly + 500)
        disable_all()


def prog_5():
    print('prog_5 started')
    dly = set_delay(6)
    for i in range(20):
        c1 = set_color1()
        c2 = set_color1()
        if c1 == c2: 
            dly = int(dly * 1.5)
            uasyncio.create_task(fade(CH1[c1], duty=1024, delay=dly))
            await uasyncio.sleep_ms(64 * dly + 100)
        else:
            uasyncio.create_task(fade(CH1[c1], duty=1024, delay=dly))
            await uasyncio.sleep_ms(64 * dly + 100)
            uasyncio.create_task(fade(CH1[c2], duty=1024, delay=dly))
            await uasyncio.sleep_ms(128 * dly + 100)
        c1 = set_color1()
        c2 = set_color1()
        if c1 == c2: 
            dly = int(dly * 1.5)
            uasyncio.create_task(fade(CH2[c1], duty=1024, delay=dly))
            await uasyncio.sleep_ms(64 * dly + 100)
        else:
            uasyncio.create_task(fade(CH2[c1], duty=1024, delay=dly))
            await uasyncio.sleep_ms(64 * dly + 100)
            uasyncio.create_task(fade(CH2[c2], duty=1024, delay=dly))
            await uasyncio.sleep_ms(128 * dly + 100)
        #await uasyncio.sleep_ms(2000)
        disable_all()


def prog_6():
    print('prog_6 started')
    dly = set_delay(6)
    for i in range(10):
        for j in range(3):
            color = set_color()
            uasyncio.create_task(fade_up(CH1[j], duty=color[j], delay=dly))
        for j in range(3):
            color = set_color()
            uasyncio.create_task(fade_up(CH2[j], duty=color[j], delay=dly))
        await uasyncio.sleep_ms(128 * dly + 1000)
        disable_all()


def prog_7():
    print('prog_7 started')
    uasyncio.create_task(flame(r1, g1))
    uasyncio.create_task(flame(r2, g2))
    await uasyncio.sleep_ms(20_000)
    disable_all()


def prog_8():
    print('prog_8 started')
    dly = set_delay(6)
    for count in range(20):
        c1 = set_color()
        c2 = set_color()
        for j in range(3):
            uasyncio.create_task(fade_up(CH1[j], duty=c1[j], delay=dly))
            uasyncio.create_task(fade_down(CH2[j], duty=c2[j], delay=dly))
        await uasyncio.sleep_ms(64 * dly + 500)
        disable_all()


def prog_9():
    print('prog_9 started')
    for i in range(50):
        c1 = set_color()
        c2 = set_color()
        for j in range(3):
            uasyncio.create_task(blink(CH1[j], \
                duty=c1[j], period_on=500, period_off=1))
            uasyncio.create_task(blink(CH2[j], \
                duty=c2[j], period_on=500, period_off=1))
            await uasyncio.sleep_ms(501)
            uasyncio.create_task(blink(CH1[j], \
                duty=c1[j], period_on=500, period_off=1))
            uasyncio.create_task(blink(CH2[j], \
                duty=c2[j], period_on=500, period_off=1))
            await uasyncio.sleep_ms(501)
            uasyncio.create_task(blink(CH1[j], \
                duty=c1[j], period_on=500, period_off=1))
            uasyncio.create_task(blink(CH2[j], \
                duty=c2[j], period_on=500, period_off=1))
        #await uasyncio.sleep_ms(501)
        disable_all()


def prog_10():
    print('prog_10 started')
    dly = set_delay(6)
    for i in range(30):
        c1 = set_color()
        c2 = set_color()
        for j in range(3):
            uasyncio.create_task(fade(CH1[j], duty=c1[j], delay=dly))
            uasyncio.create_task(fade(CH2[j], duty=c2[j], delay=dly))
        await uasyncio.sleep_ms(128 * dly + 500)
        disable_all()


def prog_11():
    print('prog_11 started')
    dly = set_delay(6)
    for i in range(30):
        color1 = set_color()
        color2 = set_color()
        for j in range(3):
            uasyncio.create_task(fade_up(CH1[j], duty=color1[j], delay=1))
        await uasyncio.sleep_ms(80)
        for j in range(3):
            uasyncio.create_task(fade_down(CH1[j], duty=color1[j], delay=dly))
        await uasyncio.sleep_ms(64 * dly + 1000)
        for j in range(3):
            uasyncio.create_task(fade_up(CH2[j], duty=color2[j], delay=1))
        await uasyncio.sleep_ms(80)
        for j in range(3):
            uasyncio.create_task(fade_down(CH2[j], duty=color2[j], delay=dly))
        await uasyncio.sleep_ms(64 * dly + 1000)
        for j in range(3):
            uasyncio.create_task(fade_up(CH1[j], duty=color1[j], delay=1))
            uasyncio.create_task(fade_up(CH2[j], duty=color2[j], delay=1))
        #await uasyncio.sleep_ms(100)
        await uasyncio.sleep_ms(64 * dly + 1000)
        disable_all()


def prog_12():
    print('prog_12 started')
    color = set_color(num=3)
    for i in range(50):
        dly = set_delay(10)
        for j in range(3):
            uasyncio.create_task(blink(CH1[j], duty=color[j], period_on=20, \
                period_off=500))
        await uasyncio.sleep_ms(dly)
        for j in range(3):
            uasyncio.create_task(blink(CH2[j], duty=color[j], period_on=20, \
                period_off=500))
        await uasyncio.sleep_ms(dly)
    disable_all()


disable_all()
#time.sleep_ms(500)
wifi.start()
while True:
    uasyncio.run(prog_1())
    time.sleep_ms(1000)
    uasyncio.run(prog_2())
    time.sleep_ms(1000)
    uasyncio.run(prog_3())
    time.sleep_ms(1000)
    uasyncio.run(prog_4())
    time.sleep_ms(1000)
    uasyncio.run(prog_5())
    time.sleep_ms(1000)
    uasyncio.run(prog_6())
    time.sleep_ms(1000)
    uasyncio.run(prog_7())
    time.sleep_ms(1000)
    uasyncio.run(prog_8())
    time.sleep_ms(1000)
    uasyncio.run(prog_9())
    time.sleep_ms(1000)
    uasyncio.run(prog_10())
    time.sleep_ms(1000)
    uasyncio.run(prog_11())
    time.sleep_ms(1000)
    uasyncio.run(prog_12())
    disable_all()
    time.sleep_ms(1000)
