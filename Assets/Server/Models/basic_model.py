
# Import libraries
from mesa import Model
from mesa.space import SingleGrid
from converter import list_to_json

# Import Agents for the Model Street
from Models.basic_agent import BasicAgent
from mesa.datacollection import DataCollector


#Import mesa
from mesa import Model 

# Debido a que necesitamos que existe un solo agente por celda, elegimos ''SingleGrid''.
from mesa.space import SingleGrid

# Con ''BaseScheduler'', hacemos que los agentes se activen ''uno a uno''.
from mesa.time import BaseScheduler


# Importamos los siguientes paquetes para el mejor manejo de valores numéricos.
import numpy as np

def get_grid(model):
  grid = np.zeros( (model.grid.width, model.grid.height) ) 
  for (content, x, y) in model.grid.coord_iter():
    if not model.grid.is_cell_empty((x, y)):
      grid[x][y] = content.isActive
  return grid

def get_ids(model):
  grid = np.zeros( (model.grid.width, model.grid.height) )
  for (content, x, y) in model.grid.coord_iter():
    if (content == None):
      grid[x][y] = 0
    else:
      grid[x][y] = content.unique_id
  return grid

class BasicModel (Model):
    def __init__(self, width = 3, height = 1000):
        self.num_agents = 300
        self.c_agents = 0
        self.width = width
        self.grid = SingleGrid(width, height, False)
        self.schedule = BaseScheduler(self)
        self.stop_distance = 25
        self.kill_agent = []
        self.step_count = 0
        self.datacollector = DataCollector(model_reporters = {"Grid" : get_grid})

        #Creación de agentes y posicionamiento en grid
        x = np.random.choice([0, 1, 2])
        a = BasicAgent(0, self, x, 0)
        self.grid.place_agent(a, (x, 0))
        self.schedule.add(a)
        self.c_agents += 1

    def step(self):  

      # Los agentes dan un paso
      self.datacollector.collect(self)
      self.schedule.step()

      #Sumo 1 a los pasos ralizados
      self.step_count += 1

      # Agregamos agente si no se ha llegado al límite de agentes
      if self.c_agents < self.num_agents and self.c_agents >= 1:
        x = np.random.choice([0, 1, 2])
        a = BasicAgent(self.c_agents, self, x, 0)
        self.grid.place_agent(a, (x, 0))
        self.schedule.add(a)
        self.c_agents += 1

      # Destruimos a los agentes que estan fuera de los límites
      for agent in self.kill_agent:
        self.schedule.remove(agent)
                
      self.kill_agent = []

      # Get information of the street

    def __str__(self):
        return f"Rails: {self.width}, Max Cars per rail: {self.height}, Number of cars: {self.c_agents}"

    def json(self):
        # Get position of the cars
        positions_list = []
        for idx in range(0, len(self.schedule.agents)):
            p = self.schedule.agents[idx].json()
            positions_list.append(p)
        positions = positions_list
        return {"Cars" : list_to_json(positions)}
        # "Rails": self.width, "Max Cars per rail": self.height, "max_num_cars": self.num_agents, "step_count": self.step_count,
