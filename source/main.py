#Based of off pybluez example rfcomm
from bluetooth import *

import random, time

import bt_server
import bt_client
import scan

def tossUp(addr, res):
    if res < 5:
        server.serverBt()
    else:
        client.clientBt(addr)


def randomGenerator():
    return random.randint(0,10)

def main():
    print("Hello")
    addr = False
    while addr == False:
        addr = scan.selectDevice()

    while True:
        try:
            if addr != False:
                res = randomGenerator()
                tossUp(addr, res)

            time.sleep(1)
        except BluetoothError:
            pass


main()
