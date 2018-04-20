#!/usr/bin/env python -u

# The -u above makes output unbuffered, which is important.

"""
Connects over USB/serial to all connected POZYX devices, finds the positions
of all devices as quickly as possible, and prints the positions to stdout

Position format: One line per record, comma-separated:
tag ID (hexadecimal) , x (meters), y (meters), z (meters) \n

"""

import threading
import sys
import os
import time
from pypozyx import *
from pozyx_localize import PozyxLocalize
import anchors

def main():
    serial_ports = get_pozyx_serial_ports()

    if len(serial_ports) == 0:
        sys.stderr.write('Warning: No Pozyx devices connected\n')

    threads = []
    print_lock = threading.Lock()
    stop_event = threading.Event()
    for port in serial_ports:
        thread = threading.Thread(target = lambda: pozyx_thread(port, print_lock, stop_event))
        thread.start()
        threads.append(thread)
    # Wait for interrupt
    while not stop_event.is_set():
        try:
            time.sleep(1024)
        except KeyboardInterrupt:
            stop_event.set()
    # Join all threads
    for thread in threads:
        thread.join()


def pozyx_thread(serial_port, print_lock, stop_event):
    pozyx = PozyxLocalize(serial_port.device, anchors.ANCHORS)
    pozyx_id = pozyx.getId()
    try:
        print_lock.acquire()
        sys.stderr.write('Serial port thread for {}: connected to Pozyx {:#x}\n'.format(serial_port.device, pozyx_id))
    finally:
        print_lock.release()
    while not stop_event.is_set():
        try:
            position = pozyx.getPosition();
            x_meters = position.x / 1000.0
            y_meters = position.y / 1000.0
            z_meters = position.z / 1000.0
            try:
                print_lock.acquire()
                print('{:x},{},{},{}'.format(pozyx_id, x_meters, y_meters, z_meters))
            except IOError:
                # Probably a broken pipe
                return
            finally:
                print_lock.release()
        except RuntimeError:
            pass

def get_pozyx_serial_ports():
    all_ports = get_serial_ports()
    return [port for port in all_ports if is_pozyx_port(port)]

if __name__ == "__main__":
    main()
