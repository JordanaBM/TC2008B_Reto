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

    # Variables auxiliares
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

    # Determinación del caso del agente según sus circusntancias
    canMove = True
    canMoveRight = False
    canMoveLeft = False

    # En primer lugar, buscamos si existen vecinos del mismo carril que estén en la congestión
    # En caso de existir tales vecinos, el agente activa la bandera de congestión [stuck]
    for neighbor in self.model.grid.get_neighbors(self.pos, moore = True, include_center = False, radius = 10):
      if neighbor.y > self.y and neighbor.x == self.x and neighbor.stuck:
        count += 1
    
    if count > 0:
      self.stuck = True

    # Después, comprobamos el resto de los casos:
    for neighbor in self.model.grid.get_neighbors(self.pos, moore = True, include_center = False, radius = 10):
      if neighbor.y == (self.y + 1) and neighbor.x == self.x and not neighbor.stop:
        # Si nuestros vecinos avanzan con normalidad en nuestro carril, no hay razón para que el agente tenga que frenar
        self.stop = False
        break
      elif neighbor.y > self.y and neighbor.x == self.x and neighbor.stop and neighbor.speed > 0:
        # Si hay un vecino que esté descacelerando en el mismo carril, el agente también procura descalerar,
        # activando para ello su bandera de frenado [stop] y posteriormente reduciendo su velocidad
        self.stop = True
        if self.speed > 0:
          self.speed -= acceleration
        break
      elif neighbor.y == (self.y + 1) and neighbor.x == self.x and neighbor.stop and neighbor.speed <= 0: 
        # Si hay un vecino completamente frenado enfrente del agente, éste se detiene en seco
        # y activa su bandera de frenado [stop]
        self.stop = True
        self.speed = 0
        break
      elif neighbor.y > self.y and (self.x - neighbor.x == 1 or self.x - neighbor.x == -1) and neighbor.stuck:
        # Si adelante hay un vecino de algún carril anexo que busca cambiar de carril y hay posibilidad de dejarlo
        # cambiar, le agente desacelera en función de la distancia, dejando el espacio de una casilla para el 
        # cambio de carril. Se activa también la bandera stop
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
      # Si hay un vecino delante del agente, se determina que este no podrá moverse en el actual paso de la simulación
      if neighbor.x == self.x and neighbor.y == (self.y + 1):
        canMove = False

    # Si no es posible moverse o se está en la congestión...
    if canMove == False or self.stuck == True:
      # Mientras que el agente no sea la causa de la congestión
      if self.unique_id != 30:
        if (self.x + 1 < 3) and (self.x - 1 > -1):
          # Si está en el carril del centro, se cambiará a cualquiera de los 2 carriles; siempre y cuando sea posible
          if self.model.grid.is_cell_empty((self.x + 1, self.y)) and self.model.grid.is_cell_empty((self.x - 1, self.y)):
            num = np.random.choice([0, 1])
            if num == 0:
              canMoveRight = True
            elif num == 1:
              canMoveLeft = True
        elif self.x + 1 < 3:
          # Si el carril a su derecha está dentro de los límites, se cambiará a ese carril
          if self.model.grid.is_cell_empty((self.x + 1, self.y)):
            canMoveRight = True
        elif self.x - 1 > -1:
          # Si el carril a su izquierda está dentro de los límites, se cambiará a ese carril
          if self.model.grid.is_cell_empty((self.x - 1, self.y)):
            canMoveLeft = True

    # Si es posible realizar algún movimiento...     
    if canMoveRight == True:
      # Se mueve a la carril de la derecha y se restablecen las banderas
      # stop y stuck a su valor default (desactivadas)
      if self.speed < 60:
        self.speed += acceleration
      self.stop = False
      self.stuck = False
      self.x = self.x + 1
      self.y = self.y + 1
      self.model.grid.move_agent(self, (self.x, self.y))
    elif canMoveLeft == True:
      # Se mueve a la carril de la izquierda y se restablecen las banderas
      # stop y stuck a su valor default (desactivadas)
      if self.speed < 60:
        self.speed += acceleration
      self.stop = False
      self.stuck = False
      self.x = self.x - 1
      self.y = self.y + 1
      self.model.grid.move_agent(self, (self.x, self.y))  
    elif canMove == True:
      # Movimiento para el resto de los casos
      if self.unique_id == 30:
        # El vehículo de la causa de la congestión, se mueve bajo diferentes circunstancias
        if self.y >= self.model.stop_distance and self.speed > 0:
          # Al alcanzar la distancia de frenado del modelo, éste desacelerará
          self.y = self.y + 1
          self.model.grid.move_agent(self, (self.x, self.y))
          self.speed -= acceleration
          self.stuck = True
          self.stop = True

        elif self.speed <= 0:
          # Al llegar a cero su velocidad, activará por primera vez la bandera de la congestión
          canMove = False
          self.stuck = True
          self.speed = 0
        else: 
          # Mientras no se cumplan el resto de los casos, se moverá normalmente
          self.y = self.y + 1
          self.model.grid.move_agent(self, (self.x, self.y))
      else: 
        # Se mueve naturalmente sobre su carril y mientras que su
        # velocidad sea menor a la máxima, la buscará aumentar
        if self.speed < 60:
          self.speed += acceleration

        if self.speed > 60:
          self.speed = 60

        self.y = self.y + 1
        self.model.grid.move_agent(self, (self.x, self.y))