# Commented out IPython magic to ensure Python compatibility.
from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

import numpy as np
import pandas as pd
import random

import time
import datetime

MAX_VELOCITY = 8 #m/s
MAX_ITERATIONS = 400 #200 Sweet spot Siempre tiene que ser multiplo de 2 si no, no aparece el vehiculo roto
WIDTH = 30
HEIGHT = 1000
SPAWN_COORDS = [5, 15, 25]
ANIMATION = 5 #No mover
CARRILES = [0, 1, 2]
ID_CAR = 0
CURRENT_TIME = 0
SPAWN_PROBABILITY = 5 #Probabilidad de que spawnee un auto 1 en X

CAR_VELOCITY = [8, 7, 6, 5, 4, 3, 2, 0]
FOV = 35 #Metros
DISTANCE_BETWEEN_VEHICLES = 6
COOLDOWN = 8

#Scenario 0
NUMBER_OF_CHECKPOINTS = 5
INITIAL_VALUES = [0, 0] #Firste number of cars, second average velocity


TEST_SCENARIO = 0 #1 = Sin propuesta de solucion, 0 Con propuesta de solucion

def get_grid(model):
  grid = np.zeros( (model.grid.width, model.grid.height) )
  for (content, x, y) in model.grid.coord_iter():
    if (content == None):
      grid[x][y] = 0
    elif (content.status == 1):
      grid[x][y] = 0.5
    else :
      grid[x][y] = 1
  return grid

class RoadVehicleAgent(Agent):
  def __init__(self, unique_id, model, lane, pos, status):
    super().__init__(unique_id, model)
    self.maxVelocity = MAX_VELOCITY
    self.minVelocity = 2
    self.velocity = MAX_VELOCITY
    self.lane = lane
    self.position = pos
    self.status = status
    self.currentCheckpoint = 0
    self.changingTo = 0
    self.cooldown = COOLDOWN
    self.changingLane= False
    self.distanceVehicle = None
    self.velocityFront = None
    self.distanceVehicleBack = None

  def can_move(self, x, y):
    return (x >= 0 and x < self.model.grid.width and
            y >= 0 and y < self.model.grid.height)

  def moveForward(self):
    if (self.velocity > 0):
      x = self.position[0]
      y = self.position[1] + self.velocity
      if self.can_move(x, y):
        if self.model.grid.is_cell_empty( (x, y)):
          self.position = (x, y)
          self.model.grid.move_agent(self, (x, y))
        aux = (self.currentCheckpoint * self.model.distanceBetweenCheckpoints) + self.model.distanceBetweenCheckpoints
        if y > aux and aux < 5:
          self.currentCheckpoint += 1
      else :
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)

  def accelerate(self):
    if (self.velocity != self.maxVelocity):
      for i in range(len(CAR_VELOCITY)):
        if (self.velocity == CAR_VELOCITY[i]):
          self.velocity = CAR_VELOCITY[i - 1]
          break

  def decelerate(self):
    if self.velocity != 0 :
      for i in range(len(CAR_VELOCITY)):
        if (self.velocity == CAR_VELOCITY[i]):
          self.velocity = CAR_VELOCITY[i + 1]
          break
    #Keep going until 5 meters distance
    if self.distanceVehicle != None :
      if (self.distanceVehicle >= 5):
        self.velocity = self.minVelocity

  def accelerateOrDecelerate (self):
    if self.status == 0:
      if (self.velocityFront == None):
        self.accelerate()
      else :
        if (self.velocityFront < self.velocity or self.distanceVehicle <= DISTANCE_BETWEEN_VEHICLES):
          self.decelerate()
        elif (self.velocityFront >  self.velocity):
          self.accelerate()

  def stopBroken(self):
    if (self.position[1] >= HEIGHT * 0.4 and self.velocity >=0):
      self.decelerate()

  def checkFrontDistance(self): #Calcula la distancia entre el vehiculo de enfrente, si es mayor a FOV es None
    distanceVehicle = 0
    x = self.position[0]
    y = self.position[1] + 1
    while (distanceVehicle < FOV and self.can_move(x, y)):
      if self.model.grid.is_cell_empty( (x, y) ):
        distanceVehicle += 1
        y += 1
      else:
        break

    if (distanceVehicle >= FOV or distanceVehicle == 0):
      self.distanceVehicle = None
      self.velocityFront = None
    else:
      self.distanceVehicle = distanceVehicle

  def checkFrontVelocity(self):
    if (self.distanceVehicle != None):
      x = self.position[0]
      y = self.position[1] + self.distanceVehicle + 1
      if self.can_move(x, y):
        if self.model.grid.is_cell_empty( (x, y) ) == False :
          neighbours = self.model.grid.get_neighbors((x, y), moore = False, include_center = True)
          self.velocityFront = neighbours[0].velocity

  #Testscenario 0 ------------------------------
  def checkBack(self, side):
    distanceVehicle = 0
    x = SPAWN_COORDS[self.lane + side]
    y = self.position[1] + DISTANCE_BETWEEN_VEHICLES
    while (distanceVehicle < FOV and self.can_move(x, y)):
      if self.model.grid.is_cell_empty( (x, y) ):
        distanceVehicle += 1
        y -= 1
      else:
        break

    if (distanceVehicle >= FOV):
      self.distanceVehicleBack = None
    else:
      self.distanceVehicleBack = distanceVehicle

  def canChangeLane(self, side):
    self.checkBack(side)
    if self.distanceVehicle == None:
      return False
    elif self.cooldown != 0:
      return False
    elif self.distanceVehicleBack == None:
      return True
    elif self.distanceVehicleBack > (FOV - 10):
      return True
    else:
      return False

  def animationChangingLine(self, side):
    x = self.pos[0] + (ANIMATION * side)
    y = self.pos[1] + DISTANCE_BETWEEN_VEHICLES
    if self.can_move(x, y):
      if self.model.grid.is_cell_empty( (x, y) ):
        self.model.grid.move_agent(self, (x, y))
        self.position = (x, y)
        self.changingLane = False
        self.changingTo = 0
    else:
      self.model.schedule.remove(self)
      self.model.grid.remove_agent(self)

  def changeLane(self, side):
    if (self.canChangeLane(side)):
      x = self.position[0] + (ANIMATION * side)
      y = self.position[1] + DISTANCE_BETWEEN_VEHICLES
      if self.can_move(x, y):
        if self.model.grid.is_cell_empty( (x, y) ):
          self.model.grid.move_agent(self, (x, y))
          self.position = (x, y)
          self.changingLane = True
          self.changingTo = side
          self.lane += side
          self.cooldown = COOLDOWN
      else:
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)

  def updateHighwaySpeed (self):
    x = self.lane
    y = self.currentCheckpoint
    self.model.highwaySpeed[x][y] = int( (self.model.highwaySpeed[x][y] + self.velocity) / 2 )

  def checkHighwaySpeed(self, side):
    return self.model.highwaySpeed[self.lane + side][self.currentCheckpoint]

  def checkHighwayVehicles(self, side):
    return self.model.highwayVehicles[self.lane + side][self.currentCheckpoint]

  def isBetterLane (self, laneSpeed, laneVehicles):
    if (laneSpeed > self.velocity):
      return True
    elif (laneSpeed >= self.velocity or laneVehicles < self.checkHighwayVehicles(0)):
      return True
    else :
      return False

  def testScenario0(self):
    right = 1
    left = -1
    self.updateHighwaySpeed()
    if (self.lane == 0): #Top Lane
      if self.isBetterLane(self.checkHighwaySpeed(right), self.checkHighwayVehicles(right)):
        self.changeLane(right)

    elif (self.lane == 1): #Central Lane
      if self.isBetterLane(self.checkHighwaySpeed(right), self.checkHighwayVehicles(right)):
        self.changeLane(right)
      elif self.isBetterLane(self.checkHighwaySpeed(left), self.checkHighwayVehicles(left)):
        self.changeLane(left)

    elif (self.lane == 2): #Bot Lane
      if self.isBetterLane(self.checkHighwaySpeed(left), self.checkHighwayVehicles(left)):
        self.changeLane(left)

  def testScenario1(self):
    right = 1
    left = -1
    if self.velocity == 0 and self.lane == 1 : #Central Lane
      if self.canChangeLane(right):
        self.changeLane(right)
      elif self.canChangeLane(left):
        self.changeLane(left)

  def step(self):
    if (self.changingLane):
      self.animationChangingLine(self.changingTo)
    else:
      self.checkFrontDistance()
      self.checkFrontVelocity()
      if (self.status == 1):
        self.stopBroken()

      if TEST_SCENARIO == 1 and self.status == 0: #Sin propuesta de solucion
        self.testScenario1()

      elif TEST_SCENARIO == 0 and self.status == 0: #Con propuesta de solucion
        self.testScenario0()

      self.accelerateOrDecelerate()
      self.moveForward()

    if (self.status == 0 and self.cooldown != 0):
      self.cooldown -= 1

class RoadModel(Model):
  def __init__ (self, width, height):
    self.grid = SingleGrid(width, height, False) #Torus grid NO
    self.distanceBetweenCheckpoints = int (HEIGHT / NUMBER_OF_CHECKPOINTS)
    self.schedule = SimultaneousActivation(self)
    self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

    self.highwaySpeed = np.full( (len(CARRILES), NUMBER_OF_CHECKPOINTS), INITIAL_VALUES[1])
    self.highwayVehicles = np.full( (len(CARRILES), NUMBER_OF_CHECKPOINTS), INITIAL_VALUES[0])

    #Place one car for the sake of the graphic
    global ID_CAR
    a = RoadVehicleAgent(ID_CAR, self, 0, (SPAWN_COORDS[0], 0), 0)
    ID_CAR += 1
    self.grid.place_agent(a, (SPAWN_COORDS[0], 0))
    self.schedule.add(a)

  def spawnCars(self):
    global ID_CAR
    for i in range(len(CARRILES)):
      probCar = np.random.randint(0, SPAWN_PROBABILITY) #Probabilidad de que spawnee un auto en carril i
      if (probCar == 1 and self.grid.is_cell_empty((SPAWN_COORDS[i], 0))):
        global ID_CAR
        a = RoadVehicleAgent(ID_CAR, self, i, (SPAWN_COORDS[i], 0), 0)
        ID_CAR += 1
        self.grid.place_agent(a, (SPAWN_COORDS[i], 0))
        self.schedule.add(a)
        #print (a.position)

  def brokenCar(self):
    global ID_CAR
    a = RoadVehicleAgent(ID_CAR, self, 1, (SPAWN_COORDS[1], 0), 1) #1 = central lane and 1 = status broken
    ID_CAR += 1
    self.grid.place_agent(a, (SPAWN_COORDS[1], 0))
    self.schedule.add(a)

  def numOfAgentsPerCheckpoint(self):
    aux = 0
    for i in range(len(SPAWN_COORDS)):
      for j in range(HEIGHT):
        if not self.grid.is_cell_empty( (SPAWN_COORDS[i], j) ):
          aux += 1
        if ((j % self.distanceBetweenCheckpoints == 0 and j != 0) or j == HEIGHT - 1):
          if j== 999:
            aux2 = int((j+1) / self.distanceBetweenCheckpoints)
          else:
            aux2 = int(j / self.distanceBetweenCheckpoints)
          self.highwayVehicles[i][aux2 - 1] = aux
          aux = 0
          aux2 = 0

  def step(self):
    if (MAX_ITERATIONS / 2 == CURRENT_TIME):
      self.brokenCar()
      print("Spawn Broken Car")
    else:
      self.spawnCars()
    if (TEST_SCENARIO == 0):
      self.numOfAgentsPerCheckpoint()
    self.datacollector.collect(self)
    self.schedule.step()