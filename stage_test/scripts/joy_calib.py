#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from sensor_msgs.msg import Joy
import numpy as np
import json

state = 0
throttle = 0
steering = 0

def callback(data):
  temp = np.abs(np.array(data.axes))
  global state
  global steering
  global throttle

  if state == 0:
    for i in range(len(temp)):
      if temp[i] == 1.0:
        throttle = i
        state +=1
        print "Nastaveno na cislo:", throttle
        print "2. Nastavte v ve do vychozi polohy."
  elif state == 1:
    if np.sum(temp) == 0:
      state += 1
      print "3. Nastavte osu pro ovladani zataceni do maximalni polohy"
  elif state == 2:
    for i in range(len(temp)):
      if temp[i] == 1.0:
        steering = i
        state +=1
        print "Nastaveno na cislo:", steering
        t = { 'steering': steering, 'throttle' : throttle}
        with open('./joy_calib.txt', 'w') as outfile:
          json.dump(t, outfile, indent = 2)
          print "soubor ulozen"
  else:
    rospy.signal_shutdown("Dokonceno")


def listener():

  state = 0
  throttle = 0
  steering = 0
  # In ROS, nodes are uniquely named. If two nodes with the same
  # node are launched, the previous one is kicked off. The
  # anonymous=True flag means that rospy will choose a unique
  # name for our 'listener' node so that multiple listeners can
  # run simultaneously.
  rospy.init_node('joy_calib', anonymous=True)

  rospy.Subscriber("joy", Joy, callback)

  print "Program pro zjisteni OS gamepadu"
  print "------------------------------------------------"
  print "1. Nastavte osu pro ovladani rychlosti do maximalni polohy"

  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':
  listener()
