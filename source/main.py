#Based of off pybluez example rfcomm
from bluetooth import *

import random, time, socket

import bt_server, bt_client
import wifi_server, wifi_client
import scan

def wifiTossUp(ip, res):
    if res < 5:
        wifi_server.hostServer(ip)
    else:
        wifi_client.hostClient(ip)

def btTossUp(addr, res):
    ip = 0

    if res < 5:
        ip = bt_server.hostServerBt()
    else:
        ip = bt_client.hostClientBt(addr)

    return ip


def randomGenerator():
    return random.randint(0,10)

def main():
    print("Hello")

    ip = 0
    addr = False
    while addr == False:
        addr = scan.selectDevice()

    while ip == 0:
        try:
            if addr != False:
                res = randomGenerator()
                ip = btTossUp(addr, res)

            time.sleep(1)
        except BluetoothError:
            pass

    wifiTossUp(ip, res)

main()
