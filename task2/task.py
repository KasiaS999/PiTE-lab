#
#Flight simulator. 
#Write a code in python that simulates the tilt correction of the plane (angle between plane wings and earth). 
#The program should print out current orientation, and applied tilt correction.
# (Tilt is "Roll" in this diagram https://www.novatel.com/assets/Web-Phase-2-2012/Solution-Pages/AttitudePlane.png)
#The program should run in infinite loop, until user breaks the loop. 
#Assume that plane orientation in every new simulation step is changing with random angle with gaussian distribution (the planes is experiencing "turbuence"). 
# Hint: "random.gauss(0, 2*rate_of_correction)"
#With every simulation step the orentation should be corrected, correction should be applied and printed out.
#Try to expand your implementation as best as you can. 
#Think of as many features as you can, and try implementing them.
#
#Try to expand your implementation as best as you can. 
#Think of as many features as you can, and try implementing them.
#Make intelligent use of pythons syntactic sugar (overloading, iterators, generators, etc)
#Most of all: CREATE GOOD, RELIABLE, READABLE CODE.
#The goal of this task is for you to SHOW YOUR BEST python programming skills.
#Impress everyone with your skills, show off with your code.
#
#Your program must be runnable with command "python task.py".
#Show some usecases of your library in the code (print some things)
#Delete these comments before commit!
#
#Good luck.
from abc import ABC, abstractmethod
from threading import Thread
import random
import time
import logging
import sys
import os

loop_delay = 0.25
if_run = True
logging.basicConfig(stream = sys.stdout,level = logging.DEBUG)

class Events(ABC):
  @abstractmethod
  def generate_event(self):
    pass

class Turbulance(Events):

  def generate_event(self, rate_of_correction):
    turbulence = random.gauss(0, 2*rate_of_correction)
    return turbulence


class Correction(Events):

  def generate_event(self, turbulence):
      correction = -(turbulence*(random.randrange(9999, 10022, 1)/10000))
      return correction

  
class Environment:
  def __init__(self, turbulance):
    self.turbulance = turbulance
    self.turbulances_rate = 2
    
  def create_turbulances(self):
    global if_run 
    while if_run:  
      one_turbulance = self.turbulance.generate_event(self.turbulances_rate)
      
      yield one_turbulance
        

class Plane:
    
    def __init__(self,roll, correction):
      self.roll = roll
      self.correction = correction


turbulences = Turbulance()
environment = Environment(turbulences)
correction = Correction()
plane = Plane(0, correction)

def turbulence_and_correction_loop(): 
    for turbulence in environment.create_turbulances():
        correction = plane.correction.generate_event(turbulence)
        plane.roll += correction+turbulence
        logging.info("\nturbulance: {}, \ncorrection: {}, \nroll after correction {} \n\n Press Enter to stop ".format(turbulence,correction, plane.roll))
        time.sleep(loop_delay)
        os.system('clear')


def take_input():
    input()
   

if __name__ == "__main__":
    
    t1 = Thread(target = turbulence_and_correction_loop)
    t2 = Thread(target = take_input)
    t2.start()
    t1.start()
    t2.join()
    if_run = False
   
