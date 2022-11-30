# Import libraries
from mesa import Agent
import numpy as np

class SimulationAgent (Agent):
  def __init__(self, unique_id, model, x, y):
    # Creación del agente
    super().__init__(unique_id, model)
        
    # Atributos: Velocidad, posición
    self.x = x
    self.y = y
    self.speed = 60
    self.isActive = True
    # self.canMove = True
        
  def step(self):
    # Destrucción de agente en caso de llegar al límite
    if self.model.grid.out_of_bounds((self.x, (self.y + 1))):
      self.model.grid.remove_agent(self)
      self.model.kill_agent.append(self)
      self.isActive = False

    if not self.isActive:
      return

    # Revisar vecinos y cambiar de posición
    # print(self.unique_id)
    canMove = True
    canMoveRight = False
    canMoveLeft = False

    for neighbor in self.model.grid.get_neighbors(self.pos, moore = True, include_center = False):
      if neighbor.x == self.x and neighbor.y == (self.y + 1):
        canMove = False

        if (self.x + 1 < 3) and (self.x - 1 > -1):
          if self.model.grid.is_cell_empty((self.x + 1, self.y)) and self.model.grid.is_cell_empty((self.x - 1, self.y)):
            num = np.random.choice([0, 1])
            if num == 0:
              print("Derecha-1")
              canMoveRight = True
            elif num == 1:
              print("Izquierda-1")
              canMoveLeft = True
        elif self.x + 1 < 3:
          if self.model.grid.is_cell_empty((self.x + 1, self.y)):
            print("Derecha")
            canMoveRight = True
        elif self.x - 1 > -1:
          if self.model.grid.is_cell_empty((self.x - 1, self.y)):
            print("Izquierda")
            canMoveLeft = True
              
    # Si no hay alguien adelante, se mueve adelante        
    if canMove == True:
      if self.unique_id == 30 and self.model.stop_distance <= self.y:
        canMove = False
      else: 
        self.y = self.y + 1
        self.model.grid.move_agent(self, (self.x, self.y))
    elif canMoveRight == True:
      self.x = self.x + 1
      self.model.grid.move_agent(self, (self.x, self.y))
    elif canMoveLeft == True:
      self.x = self.x - 1
      self.model.grid.move_agent(self, (self.x, self.y))

  def json(self):
        return {"unique_id": int(self.unique_id), "x":  int(self.x), "y": int(self.y), "speed": float(self.speed)}

  def __str__(self):
        return f"Car ID: {self.unique_id}, Position x: {self.x}, Position y: {self.x}, Speed: {self.speed}"

   