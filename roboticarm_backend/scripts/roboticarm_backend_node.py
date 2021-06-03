#!/usr/bin/env python

from roboticarm_backend.srv import SavePoint
from roboticarm_backend.srv import DeletePoint
from roboticarm_backend.srv import SaveConfig
import rospy
import pymongo
import sys
import copy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group_name = "arm_group"
move_group = moveit_commander.MoveGroupCommander(group_name)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

pointArrary = []

def roboticarm_backend_server():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('roboticarm_backend_server')
    savepts = rospy.Service('save_point', SavePoint, save_point)
    deletepts = rospy.Service('delete_point', DeletePoint, delete_point)
    savecfg = rospy.Service('save_config', SaveConfig, save_config)
    print("Ready to save points.")
    rospy.spin()

def save_point(req):
    point = {
        "joints": move_group.get_current_joint_values(),
        "delay": req.delay
    }
    pointArrary.append(point)
    # print(pointArrary)
    return 200


def delete_point(req):
    if(len(pointArrary)!=0):
        pointArrary.pop()
        # print(pointArrary)
        return 200
    else:
        return 404


def save_config(req):
    print("called")
    return 200

if __name__ == "__main__":
    roboticarm_backend_server()