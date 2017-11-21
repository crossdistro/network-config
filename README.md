# Proof of concept network configuration playground

Show commands that would enable `profile0`:

    ./config profile0 up

Show commands that would disable `profile0`:

    ./config profile0 down

## Wireless networking

There's a simple wrapper that connects the link layer using
`wpa_supplicant`:

    ./wifi.py --ifname wlan0 --ssid your_ssid --passphrase your_psk_passphrase

## DHCP

Another simple wrapper waits for carrier and then starts dhcpcd
for the interface.

    ./dhcp.py --ifname wlan0

## Resources

  * https://github.com/NetworkManager/ansible-network-role
