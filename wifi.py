#!/usr/bin/python3

import subprocess
import argparse

def wpa_passphrase(ssid, passphrase):
    return subprocess.check_output(
        ["wpa_passphrase", ssid],
        input=passphrase, universal_newlines=True)

def wpa_supplicant(ifname, config):
    return subprocess.check_output(
        ["wpa_supplicant", "-i", ifname, "-c", "/dev/stdin"],
        input=config, universal_newlines=True)

parser = argparse.ArgumentParser()
parser.add_argument("--ifname", default="wlan0")
parser.add_argument("--ssid", required=True)
parser.add_argument("--passphrase")

options = parser.parse_args()

if not options.passphrase:
    options.passphrase = input("Enter passphrase: ")

print(options)
wpa_supplicant(options.ifname, wpa_passphrase(options.ssid, options.passphrase))
