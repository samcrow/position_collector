#!/usr/bin/env python3

"""
Finds the mean and standard deviation X, Y, and Z values from records in a CSV
file
"""

import math
import sys

def main():
    if len(sys.argv) < 2:
        print('Usage: measure_error.py csv-file')
        return
    csv_path = sys.argv[1]

    # Map from source to (x array, y array, z array)
    sources = {}
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

            if source not in sources:
                sources[source] = ([], [], [])
            sources[source][0].append(x)
            sources[source][1].append(y)
            sources[source][2].append(z)

    for source, (x_values, y_values, z_values) in sources.items():
        print('Source {}'.format(source))
        x_stats = stats(x_values)
        y_stats = stats(y_values)
        z_stats = stats(z_values)
        print('  X: mean %f m, standard deviation %f m' % x_stats)
        print('  Y: mean %f m, standard deviation %f m' % y_stats)
        print('  Z: mean %f m, standard deviation %f m' % z_stats)


# Returns the mean and standard deviation of the values. Assumes that values
# is a non-empty list.
def stats(values):
    sum = 0.0
    for value in values:
        sum += float(value)
    mean = sum / float(len(values))
    # Standard deviation section
    sum_squared_deviation = 0.0
    for value in values:
        deviation = float(value) - mean
        squared_deviation = deviation * deviation
        sum_squared_deviation += squared_deviation
    std_deviation = math.sqrt(sum_squared_deviation / float(len(values)))

    return mean, std_deviation

if __name__ == "__main__":
    main()
