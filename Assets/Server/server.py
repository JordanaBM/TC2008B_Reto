# Importamos librerías necesarias
from flask import Flask, request
import numpy as np
import json

# Importamos nuestros modelos (Básico y Avanzado)
from Models.basic_model import BasicModel, get_grid, get_ids
from Models.advanced_model import AdvancedModel, get_grid, get_ids
from converter import message_to_json, to_json

# Número de carriles
WIDTH = 3
# La longitud de la pista es las posiciones que quieras entre el tamaño de los 
# prefas en unity, en este caso 1000 metros entre 5 metros de cada carro
HEIGHT = int(1000/5)
POSITIONS = []

"""Creamos funciones auxiliares"""

#Función que devuelve el id de un agente
def take_id(POS):
    return POS[3]

#Función que obtiene del grid las posiciones de los agentes
def updatePositions():
    POSITIONS.clear()
    global model
    model.step()
    matrix = np.array(get_grid(model))
    matrix_ids = np.array(get_ids(model))
    for x in range(WIDTH):
        for z in range(HEIGHT):
            if (matrix[x, z] != 0):
                pos = [x, 0, z, matrix_ids[x, z]]
                POSITIONS.append(pos)                

#Función que obtiene una posición de un carro con su id específico 
def getPositionById(id, ps):
    pos = None
    for p in ps:
        if p[3] == id:
            pos = p
    
    return pos

#Función que convierte una posición a formato JSON
def positionsToJSON(ps):
    posDICT = []

    for p in ps:

        pos = {
            "x" : p[0],
            "y" : p[1],
            "z" : p[2],
            "id" : p[3],
        }
        posDICT.append(pos)
    return json.dumps(posDICT)

""""Creamos un servidor Flask"""
app = Flask(__name__)

# Modelo Básico o Avanzado

# model = BasicModel(3,1000)
model = AdvancedModel(3,1000)

# Endpoint para checar que el server esté prendido
@app.route('/', methods=['GET'])
def hello_world():
    return message_to_json("¡Está vivo!")

# Inicializamos el modelo
@app.route('/init', methods=['POST'])
def initial_model():
    # Obtenemos los parámetros
    width = request.json['width']
    height = request.json['height']

    global model
    # model = BasicModel( width, height)
    model = AdvancedModel( width, height)

    #Devolvemos la información del modelo
    return to_json(model.json())

# Para realizar un reset del modelo
@app.route('/reset', methods=['GET'])
def reset_model():

    global model
    # model = BasicModel()
    model = AdvancedModel()

    return message_to_json('Reset the model')

#Para obtener la posición de un carro con su id
@app.route('/position', methods=['GET'])
def modelPosition():
    args = request.args
    id = args.get('id')
    if id is not None:
        id = float(id)
        sorted_pos2 = sorted(POSITIONS, key=take_id)
        pos = getPositionById(id, sorted_pos2)
        if pos is not None:
            pos = positionsToJSON([pos])
            return pos
        else:
            resp = "No se ha creado ese carro"
        return resp
    else:
        resp = "Error con un id"
        return resp


# Para ejecutar un paso dele modelo
@app.route('/step', methods=['GET'])
def modelStep():
    updatePositions()
    sorted_pos = sorted(POSITIONS, key=take_id)
    modelPosition()
    resp = "{\"data\":" + positionsToJSON(sorted_pos) + "}"
    return resp


# Obtener la infromación inicial del modelo
@app.route('/info', methods=['GET'])
def info_model():
    return message_to_json(model.__str__())
