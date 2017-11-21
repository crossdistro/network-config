#!/usr/bin/python3

import subprocess
import argparse
import pyroute2

def wait_for_carrier(ifname):
    with pyroute2.IPRoute() as ipr:
        ipr.bind()
        while True:
            for message in ipr.get():
                if message['event'] != 'RTM_NEWLINK':
                    continue
                attrs = dict(message['attrs'])
                if attrs['IFLA_IFNAME'] != ifname:
                    continue
                if attrs.get('IFLA_CARRIER') == 1:
                    return

def dhcpcd(ifname):
    subprocess.check_call(["dhcpcd", "-dd", ifname])

parser = argparse.ArgumentParser()
parser.add_argument("--ifname", default="eth0")

options = parser.parse_args()

wait_for_carrier(options.ifname)
dhcpcd(options.ifname)
from pyroute2 import IPRoute
