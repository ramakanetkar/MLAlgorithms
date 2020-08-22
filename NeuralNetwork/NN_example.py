import numpy as np

def sigmoid(x,deriv =False):
    if deriv==True:
        return (x*(1-x))
    return 1/(1+np.exp(-x))
#input data
x = np.array([[0,0,1],[0,1,1],[1,0,1],[1,1,1]])
#output data
y = np.array([[0],[1],[1],[0]])
#seed good for debugging
np.random.seed(1)

#weights

weights1 = 2*np.random.random((3,4))-1
weights2 = 2*np.random.random((4,1))-1

for j in range(60000):
    #layers
    layer0 = x
    layer1 = sigmoid(np.dot(layer0,weights1))
    layer2 = sigmoid(np.dot(layer1,weights2))

    #backpropogation
    layer2_error = y - layer2
    if (j % 10000) == 0:
        print('Error' + str(np.mean(layer2_error)))
    layer2_delta = layer2_error *sigmoid(layer2,deriv=True)

    layer1_error = layer2_delta.dot(weights2.T)

    layer1_delta = layer1_error * sigmoid(layer1, deriv = True)

    weights2 += layer1.T.dot(layer2_delta)
    weights1 += layer0.T.dot(layer1_delta)

print('Training output')
print(layer2)

