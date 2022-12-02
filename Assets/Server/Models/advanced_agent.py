# Import libraries
from mesa import Agent
import numpy as np

class AdvancedAgent (Agent):
  def __init__(self, unique_id, model, x, y):
    # Creación del agente
    super().__init__(unique_id, model)
        
    # Atributos: Velocidad, posición
    self.x = x
    self.y = y
    self.speed = 60
    self.isActive = True
    self.stop = False
    self.stuck = False
    self.wait = False
  
  def step(self):

    acceleration = 6
    x_axis = 0
    count = 0

    # Destrucción de agente en caso de llegar al límite
    if self.model.grid.out_of_bounds((self.x, (self.y + 1))):
      self.model.grid.remove_agent(self)
      self.model.kill_agent.append(self)
      self.isActive = False

    if not self.isActive:
      return

    # Revisar vecinos y cambiar de posición
    canMove = True
    canMoveRight = False
    canMoveLeft = False

    for neighbor in self.model.grid.get_neighbors(self.pos, moore = True, include_center = False, radius = 10):
      if neighbor.y > self.y and neighbor.x == self.x and neighbor.stuck:
        count += 1
    
    if count > 0:
      self.stuck = True

    for neighbor in self.model.grid.get_neighbors(self.pos, moore = True, include_center = False, radius = 10):
      if neighbor.y == (self.y + 1) and neighbor.x == self.x and not neighbor.stop:
        self.stop = False
        break
      elif neighbor.y > self.y and neighbor.x == self.x and neighbor.stop and neighbor.speed > 0:
        self.stop = True
        if self.speed > 0:
          self.speed -= acceleration
        break
      elif neighbor.y == (self.y + 1) and neighbor.x == self.x and neighbor.stop and neighbor.speed <= 0: 
        self.stop = True
        self.speed = 0
        break
      elif neighbor.y > self.y and (self.x - neighbor.x == 1 or self.x - neighbor.x == -1) and neighbor.stuck:
        self.stop = True
        if self.speed > 0:
          diff = (neighbor.y - 1) - self.y
          if diff == 0:
            self.speed = 0
          else:
            self.speed -= self.speed/diff
          break
          
    if self.speed < 0:
      self.speed = 0

    for neighbor in self.model.grid.get_neighbors(self.pos, moore = True, include_center = False):
      if neighbor.x == self.x and neighbor.y == (self.y + 1):
        canMove = False

    
    if canMove == False or self.stuck == True:
      if self.unique_id != 30:
        if (self.x + 1 < 3) and (self.x - 1 > -1):
          if self.model.grid.is_cell_empty((self.x + 1, self.y)) and self.model.grid.is_cell_empty((self.x - 1, self.y)):
            num = np.random.choice([0, 1])
            if num == 0:
              canMoveRight = True
            elif num == 1:
              canMoveLeft = True
        elif self.x + 1 < 3:
          if self.model.grid.is_cell_empty((self.x + 1, self.y)):
            canMoveRight = True
        elif self.x - 1 > -1:
          if self.model.grid.is_cell_empty((self.x - 1, self.y)):
            canMoveLeft = True

    # Si no hay alguien adelante, se mueve adelante      
    if canMoveRight == True:
      if self.speed < 60:
        # print(self.unique_id, self.speed)
        self.speed += acceleration
      # print(self.unique_id, "Me muevo a la derecha", self.speed)
      self.stop = False
      self.stuck = False
      self.x = self.x + 1
      self.y = self.y + 1
      self.model.grid.move_agent(self, (self.x, self.y))
    elif canMoveLeft == True:
      if self.speed < 60:
        # print(self.unique_id, self.speed)
        self.speed += acceleration
      # print(self.unique_id, "Me muevo a la izquierda", self.speed)
      self.stop = False
      self.stuck = False
      self.x = self.x - 1
      self.y = self.y + 1
      self.model.grid.move_agent(self, (self.x, self.y))  
    elif canMove == True:
      if self.unique_id == 30:
        if self.y >= self.model.stop_distance and self.speed > 0:
          self.y = self.y + 1
          self.model.grid.move_agent(self, (self.x, self.y))
          self.speed -= acceleration
          self.stuck = True
          self.stop = True

        elif self.speed <= 0:
          canMove = False
          self.stuck = True
          self.speed = 0
        else: 
          self.y = self.y + 1
          self.model.grid.move_agent(self, (self.x, self.y))
      else: 
        if self.speed < 60:
          self.speed += acceleration

        if self.speed > 60:
          self.speed = 60

        self.y = self.y + 1
        self.model.grid.move_agent(self, (self.x, self.y))
        
    # if self.unique_id == 30:
    #   print("stop ", self.stop)
        # print(self.unique_id, self.speed)