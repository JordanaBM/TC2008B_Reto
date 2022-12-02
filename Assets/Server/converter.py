# Importamos librerías
from flask import jsonify
from flask.json import dumps

# Convertimos un string a JSON
def message_to_json(message):
    return jsonify({"message": message})

#  Convertimos una posición a JSON
def position_to_json(position):
    return jsonify({'x': position.x, 'y': position.y})

# Convertimos un objeto a JSON
def to_json(obj):
    return jsonify(obj)

# Convertimos una lista a JSON
def list_to_json(list):
    return dumps(list)