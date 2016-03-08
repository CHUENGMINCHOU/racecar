#!/usr/bin/python
import rospy
import numpy as np 
from operator import itemgetter
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped 
from geometry_msgs.msg import Point
from std_msgs.msg import Float32
from std_msgs.msg import Float64
import threading

class ConeDetector:

    def __init__(self):
        self.cone_sub = rospy.Subscriber("cone_location", Float32, self.phi_callback)
        self.scan_window=rospy.Publisher("laser_window", LaserScan, queue_size=4)
        self.cd_sub = rospy.Subscriber("scan", LaserScan, self.laser_callback)
        self.cd_pub = rospy.Publisher("cone_position", PointStamped, queue_size=4)
        self.stuff_pub = rospy.Publisher("stuff", Float32, queue_size=4)

        self.phi = 90
        self.stampedpoint=PointStamped()
        self.counter=0
        self.lock = threading.Lock()

    def phi_callback(self, msg):
        with self.lock:
            self.phi =+ msg.data


    def laser_callback(self,msg):
        with self.lock:
            phi = self.phi

        time=rospy.Time.now()
        if abs(phi) <= 1:
            scan = LaserScan()
            scan = msg

            debug_msg = Float32()
            debug_msg.data = msg.angle_min
            self.stuff_pub.publish(debug_msg)

            self.scan_window.publish(scan)

        else:
            scan = LaserScan()
            scan = msg
            scan.ranges = []
            self.scan_window.publish(scan)

            point=Point()
            point.x=0.0
            point.y=0.0
            point.z=0.0
            self.counter+=1
            self.stampedpoint.header.seq=self.counter
            self.stampedpoint.header.frame_id="base_link"
            self.stampedpoint.header.stamp=time
            self.stampedpoint.point=point
            self.cd_pub.publish(self.stampedpoint)
            

if __name__=="__main__":
    rospy.init_node("ConeDetector")
    node=ConeDetector()
    rospy.spin()

