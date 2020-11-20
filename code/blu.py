#!/usr/bin/env python
# --*--coding=utf-8--*--
# P191
# sudo pip install pybluez

# import time
# from bluetooth import *
#
# alreadyFound = []
#
#
# def findDevs():
#     foundDevs = discover_devices(lookup_names=True)
#     for (addr, name) in foundDevs:
#         if addr not in alreadyFound:
#             print
#             "[*] Found Bluetooth Device :  " + str(name)
#             print
#             "[+] MAC address :  " + str(addr)
#             alreadyFound.append(addr)
#
#
# while True:
#     findDevs()
#     time.sleep(5)

# d4:ca:6e:f1:6d:11

# import bluetooth
#
# nearby_devices = bluetooth.discover_devices(lookup_names=True)
# for addr, name in nearby_devices:
#     print("  %s - %s" % (addr, name))
#
#     services = bluetooth.find_service(address=addr)
#     for svc in services:
#         print("Service Name: %s" % svc["name"])
#         print("    Host:        %s" % svc["host"])
#         print("    Description: %s" % svc["description"])
#         print("    Provided By: %s" % svc["provider"])
#         print("    Protocol:    %s" % svc["protocol"])
#         print("    channel/PSM: %s" % svc["port"])
#         print("    svc classes: %s " % svc["service-classes"])
#         print("    profiles:    %s " % svc["profiles"])
#         print("    service id:  %s " % svc["service-id"])
#         print("")

import time
from bluetooth import *
from datetime import datetime

def findTgt(tgtName):
    foundDevs = discover_devices(lookup_names=True)
    for (addr, name) in foundDevs:
        if tgtName == name:
            print('[*] Found Target Device ' + tgtName)
            print('[+] With MAC Address: ' + addr)
            print('[+] Time is: ' + str(datetime.now()))


tgtName = 'd4:ca:6e:f1:6d:11'

while True:
    print('[-] Scanning for Bluetooth Device: ' + tgtName)
    findTgt(tgtName)
    time.sleep(5)