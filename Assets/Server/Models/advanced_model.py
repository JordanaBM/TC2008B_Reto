
# Import libraries
from mesa import Model
from mesa.space import SingleGrid
from converter import list_to_json

# Import Agents for the Model Street
from Models.advanced_agent import AdvancedAgent
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

class AdvancedModel (Model):
    def __init__(self, width, height):
        # Variables del modelo
        self.num_agents = 100
        self.c_agents = 0
        self.grid = SingleGrid(width, height, False)
        self.schedule = BaseScheduler(self)
        self.datacollector = DataCollector(model_reporters = {"Grid" : get_grid})
        self.stop_distance = 10
        self.kill_agent = []

        # Creación de agentes y posicionamiento en grid
        x = np.random.choice([0, 1, 2])
        a = AdvancedAgent(0, self, x, 0)
        self.grid.place_agent(a, (x, 0))
        self.schedule.add(a)
        self.c_agents += 1

    def step(self):
      # Se guarda el grid en el momento actual
      self.datacollector.collect(self)

      # Los agentes dan un paso
      self.schedule.step()

      # Agregamos agente si no se ha llegado al límite de agentes
      if self.c_agents < self.num_agents and self.c_agents >= 1:
        x = np.random.choice([0, 1, 2])
        a = AdvancedAgent(self.c_agents, self, x, 0)
        self.grid.place_agent(a, (x, 0))
        self.schedule.add(a)
        self.c_agents += 1

      # Destruimos a los agentes que estan fuera de los límites
      for agent in self.kill_agent:
        self.schedule.remove(agent)
                
      self.kill_agent = []