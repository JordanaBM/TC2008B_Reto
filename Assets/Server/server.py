# Import libraries
from flask import Flask, request
from models import SimulationModel, get_grid, get_ids
# from modelJimmy import RoadModel, get_grid, get_ids
from converter import message_to_json, to_json
import numpy as np

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

WIDTH = 3
HEIGHT = 1000
POSITIONS = []

#Create functions

def take_id(POS):
    return POS[3]

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

def getPositionById(id, ps):
    pos = None
    for p in ps:
        if p[3] == id:
            pos = p
    
    return pos


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
        # print(json.dumps(posDICT))
    return json.dumps(posDICT)





# Create the Flask app
app = Flask(__name__)

# Initialize the model
model = SimulationModel(3,1000)

# Endpoint for check the status of the server
@app.route('/', methods=['GET'])
def hello_world():
    return message_to_json("The app is running!")

# Initialize the model
@app.route('/init', methods=['POST'])
def initial_model():
    # Get the parameters
    width = request.json['width']
    height = request.json['height']

    # Initialize the model
    global model
    model = SimulationModel( width, height)

    # Return the message
    return to_json(model.json())

# Reset state of the model
@app.route('/reset', methods=['GET'])
def reset_model():

    global model
    model = SimulationModel()

    return message_to_json('Reset the model')


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
            resp = "Not created yet"
        return resp
    else:
        resp = "Error with the id ¿?"
        return resp


# Exexute step of model
@app.route('/step', methods=['GET'])
def modelStep():
    updatePositions()
    sorted_pos = sorted(POSITIONS, key=take_id)
    modelPosition()
    #print(sorted_pos)
    resp = "{\"data\":" + positionsToJSON(sorted_pos) + "}"
    #print(resp)
    return resp


# Get initial info of model
@app.route('/info', methods=['GET'])
def info_model():
    return message_to_json(model.__str__())

# Save animation of model
@app.route('/save', methods=['GET'])
def save_model():
    return message_to_json('Saving the app')