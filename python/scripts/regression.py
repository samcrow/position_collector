#!/usr/bin/env python

"""
Reads positions from a file, calculates linear regression between VR and
Pozyx tags from the first half of the file, and evaluates the regression
on the second half of the file.
"""

import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import itertools

def main():
    if len(sys.argv) != 2:
        print('Usage: plot_regression.py csv-file')
        sys.exit(-1)
    csv_path = sys.argv[1]

    linker = TimeLinker()

    with open(csv_path, 'r') as file:
        header_read = False
        for line in file:
            if not header_read:
                header_read = True
                continue
            parts = line.split(',')
            if len(parts) != 5:
                raise RuntimeError('Failed to parse line "' + line + '"')
            source = parts[0]
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            linker.record_point(source, x, y, z)

    # Create plot
    figure, axes = plt.subplots(len(linker.sources()), 3)
    figure.subplots_adjust(left = 0.05, right = 0.97, bottom = 0.07, top = 0.96, wspace = 0.16, hspace = 0.6)

    i = 0
    for source in linker.sources():
        data = linker.data_for_source(source)
        pozyx_x = [d[1][0] for d in data]
        vr_x = [d[0][0] for d in data]
        pozyx_y = [d[1][1] for d in data]
        vr_y = [d[0][1] for d in data]
        pozyx_z = [d[1][2] for d in data]
        vr_z = [d[0][2] for d in data]
        check_regression(source + ' X', pozyx_x, vr_x, axes[i][0])
        check_regression(source + ' Y', pozyx_y, vr_y, axes[i][1])
        check_regression(source + ' Z', pozyx_z, vr_z, axes[i][2])

        i += 1
    # Show graphs
    plt.show()

def check_regression(source_name, pozyx_values, vr_values, axis):
    if len(pozyx_values) != len(vr_values):
        raise RuntimeError('Non-equal lengths')
    pozyx_first = pozyx_values[:len(pozyx_values) / 2]
    vr_first = vr_values[:len(vr_values) / 2]
    print('{} to VR first half: {} values'.format(source_name, len(pozyx_first)))
    m, b = np.polyfit(pozyx_first, vr_first, 1)
    print('VR = {} * Pozyx + {}'.format(m, b))
    print('First half sum squared error: {}'.format(calculate_error(pozyx_first, vr_first, m, b)))
    pozyx_second = pozyx_values[len(pozyx_values) / 2:]
    vr_second = vr_values[len(vr_values) / 2:]
    print('Second half sum squared error: {}'.format(calculate_error(pozyx_second, vr_second, m, b)))
    # Plot things
    axis.scatter(pozyx_first, vr_first, s = 0.5, color = 'blue', alpha = 0.5)
    axis.scatter(pozyx_second, vr_second, s = 0.5, color = 'green', alpha = 0.5)
    x_range = 1
    axis.plot([-x_range, x_range], [-x_range * m + b, x_range * m + b], scalex = False, scaley = False, color = 'red')
    axis.set_xlabel('Pozyx')
    axis.set_ylabel('VR')
    axis.set_title(source_name)

def calculate_error(x_values, y_values, m, b):
    sum = 0
    for x, y in itertools.izip(x_values, y_values):
        expected_y = m * x + b
        error = y - expected_y
        sum += error ** 2
    return sum


# Associates each non-VR point with the most recent VR point
class TimeLinker(object):
    def __init__(self):
        # Map from source (not VR) to an array of (position, vr_position)
        # tuples. Each tuple is (x, y, z).
        self.map = {}
        # Last VR point (x, y, z)
        self.last_vr = None
    def record_point(self, source, x, y, z):
        if source == 'VR':
            self.last_vr = (x, y, z)
        else:
            if self.last_vr != None:
                if source not in self.map:
                    self.map[source] = []
                self.map[source].append(((x, y, z), self.last_vr))
    # Returns an array/enumerable thing containing the sources in this map
    def sources(self):
        return self.map.keys()
    # Returns an array (position, vr_position) tuples for the
    # provided source
    def data_for_source(self, source):
        return self.map[source]

if __name__ == "__main__":
    main()
