import bluetooth

def printDevices(nearby_devices):
    i = 0
    for addr, name in nearby_devices:
        print("%d. %s - %s" % (i+1, addr, name))
        i+=1
    return i

def chooseDevice(nearby_devices, res):
    i = 1
    for addr, name in nearby_devices:
        if i == res:
            return addr
        print("%d. %s - %s" % (i, addr, name))
        i+=1
    return False


def selectDevice():
    print("Scanning...")

    nearby_devices = bluetooth.discover_devices(
        duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

    count = printDevices(nearby_devices)

    if count != 0:
        print("Choose which Device you would like to connect with:")
        res = int(raw_input())
    else:
        print("No Devices found. Restarting...")
        return False

    if res > count and not isinstance(res, int):
        return False

    addr = chooseDevice(nearby_devices,  res)

    return addr
