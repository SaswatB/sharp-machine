import numpy as np

def train(X, Y):
    for i in range(0, len(X)):
        X[i].insert(0, 1)
    X = np.matrix(X)
    Y = np.transpose(np.matrix([Y]))

    w = np.matmul(
           np.matmul(
              np.linalg.pinv(
                 np.matmul(
                    np.transpose(X),
                    X)),
              np.transpose(X)),
           Y)
    return {"model": w}

def vecMultiply(x, w):
    res = 0
    for i in range(0, len(x)):
        res += w[i]*x[i]
    return res

def sign(x):
    return 1 if x > 0 else -1

def evaluate(w, x):
    return sign(vecMultiply(w, x))

def getName():
    return "Linear Regression"

def getRequiredParameters():
    return []

def getOptionalParameters():
    return []

if __name__ == "__main__":
    X = [[1, 2],[2, 3],[1, 1]]
    Y = [-1, 1, -1]
    print train(X, Y)
