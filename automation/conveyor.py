
import logging
log = logging.getLogger(__name__)


import threading
from time import time, sleep


class Conveyor():   
    
    def __init__(self, name, mm, axis, uStep, default_speed=100, default_accel=100, direction="positive", gain= 157):

        self.name = name
        self.mm = mm
        self.axis = axis
        self.direction = direction
        self.speed = default_speed
        self.accel = default_accel
        self.gain = gain
        self.uStep = uStep
        
        self.mm.configAxis(self.axis, self.uStep, self.gain)

        if direction == "negative":
            self.speed = speed*-1
 
    def stop_rolling(self):
        self.mm.setContinuousMove(self.axis, self.speed, self.accel)
        
    def start_rolling(self):
        self.mm.stopContinuousMove(self.axis, self.accel)
 