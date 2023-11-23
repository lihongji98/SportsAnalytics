import numpy as np
import pandas as pd
import time

class logistic:
    def __init__(self) -> None:
        # y = 1 / (1 + exp{-(Ax + B)})
        self.data_num, self.feature_num = None, None
        self.A, self.B = None, None
        self.vector_A, self.vector_B = 0, 0
        self.momentum = 0.9
    
    def train(self, X, Y, epochs=100, lr = 3e-4):
        self.data_num = X.shape[0]
        self.feature_num = X.shape[1]
        self.A = np.random.normal(-0.1, 0.1, size=(self.feature_num, 1))
        self.B = np.random.normal(0, 0, size=(self.data_num, 1))

        assert X.shape == (self.data_num, self.feature_num), \
                                            "The shape of training data is not compatible with this model."
        assert Y.shape == (self.data_num, 1), \
                                            "The shape of label data is not compatible with this model."
        
        for epoch in range(epochs):
            d_A = np.dot(X.T, self.infer(X) - Y) / X.shape[0]
            d_B = np.dot((self.infer(X) - Y).T, np.float32(np.ones(shape=(self.data_num, 1)))) / X.shape[0]
            
            # loss function is cross-entropy
            loss = -(np.dot(Y.T, np.log(self.infer(X))) \
                                        + np.dot((np.float32(np.ones(shape=(self.data_num, 1))) - Y).T, 
                                                 np.log(np.float32(np.ones(shape=(self.data_num, 1))) - self.infer(X)))) / self.data_num
            
            if epoch % 1000 == 0:
                print(f"epoch : {epoch} / {epochs}, loss: {loss.flatten()[0]}")

            self.vector_A = self.momentum * self.vector_A + (1 -self.momentum) * d_A
            self.vector_B = self.momentum * self.vector_B + (1 -self.momentum) * d_B

            self.A -= lr * self.vector_A
            self.B -= lr * self.vector_B

            time.sleep(0)
    
    def infer(self, X):
        return 1 / (1 + np.exp(-(np.dot(X, self.A) + self.B)))

a = logistic()
x = [[1, 1, 1, 0, 0],[1, 0, 1, 0, 0],[1, 1, 0, 0, 0],[0, 0, 0, 0, 1],[0, 0, 0, 1, 1]]
X = np.array(x).reshape(5, 5)
Y = np.array([1,1,1,0,0]).reshape(5,1)
a.train(X, Y, epochs=1000000, lr=1e-3)
print(a.infer(X).flatten())
print(Y.flatten())
