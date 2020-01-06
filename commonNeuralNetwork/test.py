import numpy as np
from commonNN import CommonNeuralNetwork

nn = CommonNeuralNetwork((3, 4, 1))
print(nn.get_result(np.array([[1, 1, 1]])))
X = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

y = np.array([[0],
              [1],
              [1],
              [0]])
# print(f'длина={len(nn.layers)}')
print(nn.get_result(X))
nn.learn_network(X, y)
print(nn.get_result(X))