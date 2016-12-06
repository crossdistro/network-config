def ip_link_set_up(interface):
    yield ["ip", "link", "set", interface, "up"]

def ip_address(add_delete, address, interface, alias=None):
    yield ["ip", "address", add_delete, address, "dev", interface] \
        + ["label", "{}:{}".format(interface, alias)] if alias else []

def ip_route(add_delete, network, gateway, interface):
    yield ["ip", "route", add_delete, network] \
        + ["via", gateway] if gateway else [] \
        + ["dev", interface] if gateway else []
