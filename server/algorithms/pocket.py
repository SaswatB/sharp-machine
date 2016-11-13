from random import shuffle

DEFAULT_MAX_ITERATIONS = 1000

def train(X, Y, iter=DEFAULT_MAX_ITERATIONS, w=-1):
    if w == -1:
        w = [0] * (len(X[0]) + 1)
    w[0] = 1

    temp = []
    for i in range(0, len(X)):
        t = [1]
        t.extend(X[i])
        temp.append(t)
    X = temp

    bestW = w
    bestErr = error(X, Y, bestW)
    
    for it in range(0, iter):
        bad_i = getBadPoint(X, Y, w)
        if bad_i == -1:
            return {"model": bestW, "iterations": iter}
        w = vecAdd(w, vecScale(X[bad_i], Y[bad_i]))
        err = error(X, Y, w)
        if err < bestW:
            bestW = w
            bestErr = err
    return {"model": bestW, "iterations": iter}

def getBadPoint(X, Y, w):
    indices = range(0, len(X))
    shuffle(indices)
    for i in indices:
        y = vecMultiply(X[i], w)
        if not isClassificationCorrect(y, Y[i]):
            return i
    return -1

def error(X, Y, w):
    err = 0
    for i in range(0, len(X)):
        y = vecMultiply(X[i], w)
        if not isClassificationCorrect(y, Y[i]):
            err += 1
    return float(err)/len(X)

def isClassificationCorrect(y1, y2):
    return (y1 < 0 and y2 < 0) or (y1 > 0 and y2 > 0) or (y1 == 0 and y2 == 0)

def vecMultiply(x, w):
    res = 0
    for i in range(0, len(x)):
        res += w[i]*x[i]
    return res

def vecAdd(x, w):
    res = [0]*len(x)
    for i in range(0, len(x)):
        res[i] = x[i]+w[i]
    return res

def vecScale(x, s):
    res = [0]*len(x)
    for i in range(0, len(x)):
        res[i] = x[i]*s
    return res

def sign(x):
    return 1 if x > 0 else -1

def evaluate(w, x):
    x = x[:]
    x.insert(0, 1)
    return sign(vecMultiply(w, x))

def getName():
    return "Linear Perceptron With Pocket"

def getRequiredParameters():
    return []

def getOptionalParameters():
    return [{"name": "Max Iterations", "default_value": DEFAULT_MAX_ITERATIONS, "type": "int"}]

if __name__ == "__main__":
    X = [[1, 2],[2, 3],[1, 1]]
    Y = [-1, 1, -1]
    print train(X, Y, DEFAULT_MAX_ITERATIONS)
