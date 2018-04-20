#!/usr/bin/env python

"""
Reads positions from a CSV file and produces graphs
Usage: plot_correlations.py csv-file
"""

import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def main():
    if len(sys.argv) != 2:
        print('Usage: plot_correlations.py csv-file')
        sys.exit(-1)
    csv_path = sys.argv[1]

    # Create plot
    figure, axes = plt.subplots(3, 1)

    # Data for figures
    # Each maps from a source to an array of (seconds, meters) tuples
    x_values = ValueMap()
    y_values = ValueMap()
    z_values = ValueMap()

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
            nanoseconds = int(parts[4])
            seconds = float(nanoseconds) * 1e-9

            x_values.append(source, seconds, x)
            y_values.append(source, seconds, y)
            z_values.append(source, seconds, z)

    # Plot
    for source in x_values.sources():
        t, x = x_values.data_for_source(source)
        axes[0].plot(t, x)
    for source in y_values.sources():
        t, y = y_values.data_for_source(source)
        axes[1].plot(t, y)
    for source in z_values.sources():
        t, z = z_values.data_for_source(source)
        axes[2].plot(t, z)

    # Labels
    axes[0].set_title('X values')
    axes[1].set_title('Y values')
    axes[2].set_title('Z values')
    for axis in axes:
        axis.set_xlabel('Seconds')
        axis.set_ylabel('Position (meters)')

    plt.show()

# Maps from a source string to an array of time/value tuples
class ValueMap(object):
    def __init__(self):
        self.map = {}
    def append(self, source, time, value):
        if source not in self.map:
            self.map[source] = []
        self.map[source].append((time, value))
    # Returns an array/enumerable thing containing the sources in this map
    def sources(self):
        return self.map.keys()
    # Returns an array of time values and an array of data values for the
    # provided source
    def data_for_source(self, source):
        tuple_array = self.map[source]
        time_values = [tv[0] for tv in tuple_array]
        data_values = [tv[1] for tv in tuple_array]
        return time_values, data_values

if __name__ == "__main__":
    main()
