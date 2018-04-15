
# Simpler interface for localization with a Pozyx device

from pypozyx import *

class PozyxLocalize(object):
    # Creates a PozyxLocalize
    #
    # serial_port: a string containing the path to the serial port file
    # to use to connect to the Pozyx device
    #
    # anchors: A list of DeviceCoordinates objects containing four
    # anchors
    def __init__(self, serial_port, anchors):
        self.serial_port = serial_port
        self.pozyx = PozyxSerial(serial_port)
        # Configure anchors
        status = self.pozyx.clearDevices()
        if status != POZYX_SUCCESS:
            self.raiseError()
        for anchor in anchors:
            status = self.pozyx.addDevice(anchor)
            if status != POZYX_SUCCESS:
                self.raiseError()
        # Set ranging/communication options for faster updates
        status = self.pozyx.setRangingProtocol(POZYX_RANGE_PROTOCOL_FAST)
        if status != POZYX_SUCCESS:
            self.raiseError()


    # Returns the current position of the Pozyx device,
    # as a Coordinates object with values in millimeters
    def getPosition(self, remote_id = None):
        position = Coordinates()
        status = self.pozyx.doPositioning(position, algorithm = POZYX_POS_ALG_TRACKING, remote_id = remote_id)
        if status != POZYX_SUCCESS:
            self.raiseError()
        return position

    # Returns the 16-bit ID of this device, as an integer
    def getId(self):
        id = SingleRegister(size = 2)
        status = self.pozyx.getNetworkId(id)
        if status != POZYX_SUCCESS:
            self.raiseError()
        return id.data[0]

    # Returns the orientation of the Pozyx device as a Quaternion object
    #
    # TODO: Is the orientation calculated here, or during the last positioning
    # operation?
    def getQuaternion(self, remote_id = None):
        quaternion = Quaternion()
        status = self.pozyx.getQuaternion(quaternion, remote_id)
        if status != POZYX_SUCCESS:
            self.raiseError()
        return quaternion


    # Raises an error containing a message derived from the Pozyx error register
    def raiseError(self):
        error_code = SingleRegister()
        self.pozyx.getErrorCode(error_code)
        message = self.pozyx.getErrorMessage(error_code)
        raise RuntimeError(message)

    def serialPort(self):
        return self.serial_port
