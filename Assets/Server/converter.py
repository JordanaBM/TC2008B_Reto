# Import libraries
from flask import jsonify
from flask.json import dumps

# Convert message to json
def message_to_json(message):
    return jsonify({"message": message})

# Convert list of cars to json
def position_to_json(position):
    return jsonify({'x': position.x, 'y': position.y})

# Convert object to json
def to_json(obj):
    return jsonify(obj)

def list_to_json(list):
    return dumps(list)