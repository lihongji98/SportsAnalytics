import numpy as np
import pandas as pd
import time

class logistic:
    def __init__(self) -> None:
        # y = 1 / (1 + exp{-(Ax + B)})
        self.data_num, self.feature_num = None, None
        self.A, self.B = None, None
    
    def train(self, X, Y, epochs=100, lr = 3e-4):
        self.data_num = X.shape[0]
        self.feature_num = X.shape[1]
        self.A = np.random.normal(-10, 10, size=(self.feature_num, 1))
        self.B = np.zeros(shape=(self.data_num, 1)) 

        assert X.shape == (self.data_num, self.feature_num), \
                                            "The shape of training data is not compatible with this model."
        assert Y.shape == (self.data_num, 1), \
                                            "The shape of label data is not compatible with this model."
        
        for epoch in range(epochs):
            A_gradient = np.dot(X.T, np.dot(X, self.A) - Y) / X.shape[0]
            B_gradient = np.dot((np.dot(X, self.A) - Y).T, np.ones(shape=(self.data_num, 1))) / X.shape[0]
            
            # cost function is cross-entropy
            loss = -(np.dot(Y.T, np.log(self.infer(X))) \
                                        + np.dot((np.ones(shape=(self.data_num, 1)) - Y).T, 
                                                 np.log(1 - self.infer(X)))) / self.data_num
            
            if epoch % 1 == 0:
                print(f"epoch : {epoch} / {epochs}, loss: {loss.flatten()[0]}")

            self.A = self.A - lr * A_gradient
            self.B = self.B - lr * B_gradient

            time.sleep(0.3)
    
    def infer(self, X):
        return (1 + (np.exp(-(np.dot(X, self.A) + self.B)) + 1))**(-1)

    def check(self):
        print(self.A.shape, self.B.shape)

a = logistic()
X = np.random.normal(size=(100, 50))
Y = np.random.randint(0, 2, 100).reshape(100, 1)
a.train(X, Y, epochs=100, lr=3e-3)