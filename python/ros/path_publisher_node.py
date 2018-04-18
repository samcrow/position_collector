#!/usr/bin/env python

"""
A Robot Operating System node that reads positions from a CSV file and
publishes them as nav_msgs/Path messages

Usage: path_publisher_node.py input-file

"""

import sys
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class PathRecord(object):
    def __init__(self, publisher, path):
        self.publisher = publisher
        self.path = path

def main():
    if len(sys.argv) != 2:
        print('Usage: path_publisher_node.py input-file')
        sys.exit(-1)
    file_path = sys.argv[1]
    rospy.init_node('path_publisher_node')

    # Map from source name to PathRecord
    path_records = {}

    with open(file_path, 'r') as file:
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

            if source not in path_records:
                # Create a Path
                path = Path()
                path.header.frame_id = "map"
                # Create a publisher for the path
                publisher = rospy.Publisher('path/' + source, Path, queue_size = 8)
                path_records[source] = PathRecord(publisher, path)

            path_record = path_records[source]
            # Create a pose
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.header.stamp = rospy.Time.from_sec(nanoseconds * 1e-9)
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = z

            path_record.path.poses.append(pose)

    # Publish paths
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        # Publish each path
        for path_record in path_records.values():
            path_record.publisher.publish(path_record.path)
        rate.sleep()

if __name__ == "__main__":
    main()
