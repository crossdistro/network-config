#!/usr/bin/python3

import subprocess
import argparse
import dbus

import logging
logging.basicConfig(format="%(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger()

class WPASupplicant(object):
    DEST = "fi.w1.wpa_supplicant1"
    PATH = "/fi/w1/wpa_supplicant1"
    INTERFACE = "fi.w1.wpa_supplicant1"

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.wpas = dbus.Interface(self._get_object(self.PATH), dbus_interface=self.INTERFACE)

    def _get_object(self, path):
        return self.bus.get_object(self.DEST, path)

    def _info(self, text):
        log.info("wpa_supplicant: " + str(text))

    def create_interface(self, ifname):
        try:
            self.wpas.CreateInterface({"Driver": "nl80211,wext", "Ifname": ifname})
        except dbus.exceptions.DBusException as e:
            if e._dbus_error_name == "fi.w1.wpa_supplicant1.InterfaceExists":
                self._info(e)
            else:
                raise
        else:
            self._info("Interface created.")

    def get_interface(self, ifname):
        return WPASupplicantInterface(self, self.wpas.GetInterface(ifname))

class WPASupplicantInterface(object):
    def __init__(self, wpas, ifpath):
        self.wpas = wpas
        self._info = wpas._info
        self.iface = dbus.Interface(self.wpas._get_object(ifpath), dbus_interface=self.wpas.INTERFACE + ".Interface")

    def connect(self, ssid, psk):
        path = self.iface.AddNetwork({"scan_ssid": 1, "auth_alg": "OPEN", "ssid": ssid, "key_mgmt": "WPA-PSK", "psk": psk})
        self.iface.SelectNetwork(path)
        self._info("Connected to '{}'.".format(ssid))

def wpa_connect(ifname, ssid, psk):
    wpas = WPASupplicant()
    wpas.create_interface(ifname)
    iface = wpas.get_interface(ifname)
    iface.connect(ssid, psk)

# You can see two additional calls used by NetworkManager related to
# scanning:
#
# method call sender=:1.28 -> dest=:1.15 serial=116 path=/fi/w1/wpa_supplicant1/Interfaces/3; interface=fi.w1.wpa_supplicant1.Interface; member=Scan
#    array [
#       dict entry(
#          string "Type"
#          variant             string "active"
#       )
#    ]
#
# method call sender=:1.28 -> dest=:1.15 serial=167 path=/fi/w1/wpa_supplicant1/Interfaces/3; interface=org.freedesktop.DBus.Properties; member=Set
#    string "fi.w1.wpa_supplicant1.Interface"
#    string "ApScan"
#    variant       uint32 1

# You can see the original way I used to spawn a separate wpa_supplicant
# just for the interface:
#
# def wpa_passphrase(ssid, passphrase):
#     return subprocess.check_output(
#         ["wpa_passphrase", ssid],
#         input=passphrase, universal_newlines=True)
# 
# def wpa_supplicant(ifname, config):
#     return subprocess.check_output(
#         ["wpa_supplicant", "-i", ifname, "-c", "/dev/stdin"],
#         input=config, universal_newlines=True)
# 
# wpa_supplicant(options.ifname, wpa_passphrase(options.ssid, options.passphrase))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifname", default="wlan0")
    parser.add_argument("--ssid", required=True)
    parser.add_argument("--psk")

    options = parser.parse_args()

    #if not options.passphrase:
    #    options.passphrase = input("Enter passphrase: ")

    log.debug(options)

    wpa_connect(options.ifname, options.ssid, options.psk)
