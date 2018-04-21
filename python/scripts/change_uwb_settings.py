#!/usr/bin/env python

"""
Changes the UWB communication settings on one local Pozyx and all Pozyxes
that can be reached wirelessly with the initial communication settings
"""

import sys
from pypozyx import *

# Meanings of UWBSettings fields: https://www.pozyx.io/Documentation/Datasheet/RegisterOverview
# Target settings to change to
TARGET_SETTINGS = UWBSettings(
    # 5 = 6489.6 MHz
    channel = 5,
    # 2 = 6.8 Mbps
    bitrate = 2,
    # pulse repetition frequency 2 = 64 MHz
    prf = 2,
    # Preamble length
    plen = 0x04,
    # Gain
    gain_db = 11.5
)

# Number of remote devices that should be found
EXPECTED_REMOTE_DEVICES = 8


def main():
    port = get_serial_port()
    if port == None:
        print('No serial port found')
        sys.exit(-1)
    print('Using serial port ' + port)

    pozyx = PozyxSerial(port)

    # Reset device list
    status = pozyx.clearDevices()
    if status != POZYX_SUCCESS:
        raise RuntimeError('Failed to clear device list')


    # Repeat discovery until enough devices have been found
    device_ids = []
    while len(device_ids) < EXPECTED_REMOTE_DEVICES:
        # Search for devices
        status = pozyx.doDiscovery(POZYX_DISCOVERY_ALL_DEVICES, slots = 9, slot_duration = 0.1)
        if status != POZYX_SUCCESS:
            raise RuntimeError('Failed to discover devices')
        # Print found devices
        device_count = SingleRegister()
        status = pozyx.getDeviceListSize(device_count)
        if status != POZYX_SUCCESS:
            raise RuntimeError('Failed to get device count')

        # Extract number of devices
        device_count = device_count[0]
        if device_count < 1:
            print('No devices discovered, trying again...')
            continue
        # Get IDs of devices
        temp_ids = DeviceList(list_size = device_count)
        status = pozyx.getDeviceIds(temp_ids)
        if status != POZYX_SUCCESS:
            raise RuntimeError('Failed to get tag IDs: {}'.format(status))
        # Clear device_ids and copy in temp_ids
        del device_ids[:]
        for id in temp_ids:
            device_ids.append(id)
        if len(device_ids) < EXPECTED_REMOTE_DEVICES:
            print('Found only {} of {} expected remote devices, trying again...'
                .format(len(device_ids), EXPECTED_REMOTE_DEVICES))
    print('Found devices: {}'.format(device_ids))

    print('Saving UWB settings on remote devices...')
    for remote_id in device_ids:
        status = pozyx.setUWBSettings(TARGET_SETTINGS, remote_id = remote_id)
        if status != POZYX_SUCCESS:
            print('Warning: Failed to set UWB settings on remote device {:#x}'.format(remote_id))
        status = pozyx.saveUWBSettings(remote_id = remote_id)
        if status != POZYX_SUCCESS:
            print('Warning: Failed to save UWB settings on remote device {:#x}'.format(remote_id))


    print('Saving UWB settings on local device...')
    status = pozyx.setUWBSettings(TARGET_SETTINGS)
    if status != POZYX_SUCCESS:
        print('Warning: Failed to set UWB settings on local device')
    status = pozyx.saveUWBSettings()
    if status != POZYX_SUCCESS:
        print('Warning: Failed to save UWB settings on local device')



def get_serial_port():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        return get_first_pozyx_serial_port()

if __name__ == "__main__":
    main()
