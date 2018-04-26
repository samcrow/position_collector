#!/usr/bin/env python

"""
Reads positions from a CSV file and produces graphs
Usage: plot_regression.py csv-file
"""

import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def main():
    if len(sys.argv) != 2:
        print('Usage: plot_regression.py csv-file')
        sys.exit(-1)
    csv_path = sys.argv[1]

    # Create plot
    figure, axes = plt.subplots(1, 3)

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


    # X
    for source in linker.sources():
        data = linker.data_for_source(source)
        vr_values = [d[1][0] for d in data]
        values = [d[0][0] for d in data]
        axes[0].scatter(vr_values, values, s = 1)
    # Y
    for source in linker.sources():
        data = linker.data_for_source(source)
        vr_values = [d[1][1] for d in data]
        values = [d[0][1] for d in data]
        axes[1].scatter(vr_values, values, s = 1)
    # Z
    for source in linker.sources():
        data = linker.data_for_source(source)
        vr_values = [d[1][2] for d in data]
        values = [d[0][2] for d in data]
        axes[2].scatter(vr_values, values, s = 1)

    # Labels
    axes[0].set_title('X values')
    axes[1].set_title('Y values')
    axes[2].set_title('Z values')
    for axis in axes:
        axis.set_xlabel('VR position')
        axis.set_ylabel('Pozyx position')
        # Plot 1:1 line
        one_to_one = [-0.5, 0.5]
        axis.plot(one_to_one, one_to_one)

    plt.show()



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
