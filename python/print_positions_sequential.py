#!/usr/bin/env python

"""
Connects over USB/serial to all connected POZYX devices, finds the positions
of all devices as quickly as possible, and prints the positions to stdout

Position format: One line per record, comma-separated:
tag ID (hexadecimal) , x (meters), y (meters), z (meters) \n

"""

import threading
import sys
import time
from pypozyx import *
from pozyx_localize import PozyxLocalize
import anchors

def main():
    serial_ports = get_pozyx_serial_ports()

    if len(serial_ports) == 0:
        sys.stderr.write('Warning: No Pozyx devices connected\n')

    # List of (ID, PozyxSerial)
    pozyxes = []
    for port in serial_ports:
        pozyx = PozyxLocalize(port.device, anchors.ANCHORS)
        pozyx_id = pozyx.getId()
        pozyxes.append((pozyx_id, pozyx))
    try:
        while True:
            for pozyx_id, pozyx in pozyxes:
                try:
                    position = pozyx.getPosition();
                    x_meters = position.x / 1000.0
                    y_meters = position.y / 1000.0
                    z_meters = position.z / 1000.0
                    print('{:x},{},{},{}'.format(pozyx_id, x_meters, y_meters, z_meters))
                except IOError:
                    # Probably a broken pipe
                    return
                except RuntimeError as e:
                    # Print and ignore
                    sys.stderr.write(str(e) + '\n')

    except KeyboardInterrupt:
        return

def get_pozyx_serial_ports():
    all_ports = get_serial_ports()
    return [port for port in all_ports if is_pozyx_port(port)]

if __name__ == "__main__":
    main()
