#!/usr/bin/env python

from geometry_msgs.msg import PoseStamped
import rospy
import rosbag
import sys

"""
Reads a CSV file with positions and stores the positions in a ROS bag file
"""

def main():
    if len(sys.argv) != 3:
        print('Usage: csv_to_bag.py source-csv-file destination-bag-file')
        sys.exit(-1)
    csv_path = sys.argv[1]
    bag_path = sys.argv[2]

    with open(csv_path, 'r') as file:
        with rosbag.Bag(bag_path, 'w') as bag:
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
                # Create a pose
                pose = PoseStamped()
                pose.header.frame_id = 'map'
                pose.header.stamp = rospy.Time.from_sec(nanoseconds * 1e-9)
                pose.pose.position.x = x
                pose.pose.position.y = y
                pose.pose.position.z = z
                # Add to the bag
                bag.write('/' + source, pose)

if __name__ == "__main__":
    main()
