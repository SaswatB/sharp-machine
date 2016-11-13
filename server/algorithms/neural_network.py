import numpy as np
from numpy import tanh

DEFAULT_EPOCHS = 1000
DEFAULT_LAYERS = []
DEFAULT_LEARNING_RATE = 0.1

def make_mlp(*dimensions):
    def mlp((acc, i), y):
        return [np.random.randn(y+1, i)] + acc, y
    return reduce(mlp, dimensions[::-1], ([], 1))[0]


def sigmoid(x):
    return tanh(x)


def sigmoid_(x):
    return 1 - np.multiply(x, x)


def augment_1(v):
    return np.insert(v, 0, 1).reshape(len(v)+1, 1)


def forward_propagation(mlp, x):
    def forward(input, w):
        return input + [augment_1(sigmoid(np.dot(w.T, input[-1])))]
    return reduce(forward, mlp, [augment_1(x)])


def backpropagation(mlp, x, y):

    x_L = x[-1][1:]
    d_0 = 2*(x_L - y) * sigmoid_(x_L)
    def backward(input, (w, x)):
        delta_prev = input[0]
        delta_curr = (np.multiply(sigmoid_(x), np.matmul(w, delta_prev)))[1:]
        return [delta_curr] + input
    wx_drop1 = zip(mlp, x[:-1])[1:]
    return reduce(backward, wx_drop1[::-1], [d_0])


def train_mlp(mlp, x, y, eta=0.1, epochs=DEFAULT_EPOCHS):
    while epochs > 0:
        for x_, y_ in zip(x, y):
            signals         = forward_propagation(mlp, x_)
            sensitivities   = backpropagation(mlp, signals, y_)

            mlp = [
                w_ + -eta * np.matmul(s_, d_.T)
                    for w_,s_,d_ in zip(mlp, signals[:-1], sensitivities)
                ]
        epochs -= 1
    return mlp


def evaluate(mlp, x):
    def forward(input, w):
        return augment_1(sigmoid(np.dot(w.T, input)))
    return reduce(forward, mlp, augment_1(x))[1][0]

def sign(x):
    return 1 if x > 0 else -1

def train(X, Y, layers=DEFAULT_LAYERS, epochs=DEFAULT_EPOCHS, learning_rate=DEFAULT_LEARNING_RATE):
     print X, Y
     temp = []
     for i in range(0, len(X)):
        temp.append(np.asarray([ 1, 0 ]).reshape(len(X[i]), 1))
     X = temp
     layers.insert(0, len(X[i]))
     arch = make_mlp(*layers)
     return {"model": train_mlp(arch, X, Y)}

def getName():
    return "Neural Network"

def getRequiredParameters():
    return []

def getOptionalParameters():
    return [{"name": "Layers", "default_value": DEFAULT_LAYERS, "type": "int list"},
            {"name": "Iterations", "default_value": DEFAULT_EPOCHS, "type": "int"},
            {"name": "Learning Rate", "default_value": DEFAULT_LEARNING_RATE, "type": "float"}]

if __name__ == '__main__':
    x = [
            np.asarray([ 1, 0 ]).reshape(2, 1),
            np.asarray([ 0, 1 ]).reshape(2, 1),
            np.asarray([ 1, 1 ]).reshape(2, 1),
            np.asarray([ 0, 0 ]).reshape(2, 1)
        ]
    y = [ 1, 1, -1, -1 ]

    mlp = make_mlp(2, 2)
    mlp = train_mlp(mlp, x, y)
    for x_, y_ in zip(x, y):
        assert(sign(evaluate(mlp, x_)) == y_)
