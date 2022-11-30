# TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
# Python server to interact with Unity via POST
# Sergio Ruiz-Loza, Ph.D. March 2021

""" Importamos el modelo del archivo en que lo definimos. """
from retomultiagentes import RoadModel
from retomultiagentes import get_grid
# from models import SimulationModel, get_grid

""" Importamos los siguientes paquetes para el mejor manejo de valores
    numéricos."""
import numpy as np
import pandas as pd
import random

""" Definimos otros paquetes que vamos a usar para medir el tiempo de
    ejecución de nuestro algoritmo. """
import time
import datetime

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

WIDTH = 30
HEIGHT = 1000

model = RoadModel(WIDTH, HEIGHT)

def updatePositions():
    global model
    positions = []
    model.step()
    matrix = np.array(get_grid(model))
    #print(matrix)
    for x in range(WIDTH):
        for z in range(HEIGHT):
            if (matrix[x, z] != 0):
                pos = [x, 0, z]
                positions.append(pos)
                #print(positions)
    return positions

def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "y" : p[1],
            "z" : p[2]
        }
        posDICT.append(pos)
        print(json.dumps(posDICT))
    return json.dumps(posDICT)


class Server(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        positions = updatePositions()
        resp = "{\"data\":" + positionsToJSON(positions) + "}"
        self.wfile.write(resp.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()