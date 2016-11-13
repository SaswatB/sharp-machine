#!/usr/bin/env python
from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import send, emit
from os.path import dirname, basename, isfile
import glob
import importlib
import sys
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import io
import base64
import math

algo_files = glob.glob(dirname(__file__)+"algorithms/*.py")
algo_files = [ basename(f)[:-3] for f in algo_files if isfile(f) and not f.endswith("__init__.py")]

algorithms = {}

for file in algo_files:
    algorithm = importlib.import_module("algorithms."+file)
    if not set(["getName", "getRequiredParameters", "getOptionalParameters", "train", "evaluate"]) < set(dir(algorithm)):
        sys.stderr.write("Algorithm file \""+file+"\" missing required methods.\n")
        exit()
    algorithms[algorithm.getName()] = algorithm

def get2DBounds(data):
    x1_max = x1_min = data[0][0]
    x2_max = x2_min = data[0][1]
    
    for i in range(0, len(data)):
        print data[i]
        if data[i][0] > x1_max:
            x1_max = data[i][0]
        if data[i][0] < x1_min:
            x1_min = data[i][0]
        if data[i][1] > x2_max:
            x2_max = data[i][1]
        if data[i][1] < x2_min:
            x2_min = data[i][1]
    
    return (math.floor(x1_min), math.ceil(x1_max), math.floor(x2_min), math.ceil(x2_max))

def generateImage(algorithm, model, X, Y):
    x1_min, x1_max, x2_min, x2_max = get2DBounds(X)
    x1_min -= 1
    x1_max += 1
    x2_min -= 1
    x2_max += 1
    print (x1_min, x1_max, x2_min, x2_max)
    x1 = np.arange(x1_min, x1_max, (x1_max - x1_min)/float(100))
    x2 = np.arange(x2_max, x2_min, -(x2_max - x2_min)/float(100))
    grid = [[algorithm.evaluate(model, [x1_, x2_]) for x1_ in x1] for x2_ in x2]
    plt.imshow(grid, extent=(x1_min, x1_max, x2_min, x2_max), interpolation='none', cmap="Spectral")
    
    data_1_x1 = []
    data_1_x2 = []
    data_n1_x1 = []
    data_n1_x2 = []
    for i in range(0, len(X)):
        if Y[i] > 0:
            data_1_x1.append(X[i][0])
            data_1_x2.append(X[i][1])
        else:
            data_n1_x1.append(X[i][0])
            data_n1_x2.append(X[i][1])
    
    plt.scatter(data_1_x1, data_1_x2, color="y")
    plt.scatter(data_n1_x1, data_n1_x2, color="g")
    
    buf = io.BytesIO()
    plt.savefig(buf, format = "png")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()

def error(algorithm, model, X, Y):
    error = 0
    for i in range(0, len(X)):
        error += (algorithm.evaluate(model, X[i]) - Y[i])**2
    return error/len(X)

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def connect():
    print("connected!")
    packed_algo = []
    for a in algorithms:
        packed = {'name': a, 
                  'required_parameters': algorithms[a].getRequiredParameters(),
                  'optional_parameters': algorithms[a].getOptionalParameters()}
        packed_algo.append(packed);
    emit("init", packed_algo)

@socketio.on('train')
def handle_message(data_json):
    print('received data: ' + str(data_json))
    algorithm = algorithms[data_json["algorithm"]]
    X = []
    Y = []
    for row in data_json["data"]:
        X.append(row[:-1])
        Y.append(row[-1])
    args = {"X": X, "Y": Y}
    
    for arg in data_json.get("args",[]):
        args[arg["name"]] = arg["value"]
    result = algorithm.train(**args)
    print result
    print dir(algorithm)
    emit("result", {"result": str(result), "image": generateImage(algorithm, result["model"], X, Y), "error": error(algorithm, result["model"], X, Y)})
    print "results sent"

@app.route("/")
def hello():
    return "Server Running."

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
