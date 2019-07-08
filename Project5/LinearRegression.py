import random
import math
from Data_Utils import Get_Features
        
def get_batch(X, Y, batch_size=32):
    batch_indices = random.sample(range(len(X)), batch_size)
    batch_x = []
    batch_y = []
    index_counter = 0
    for index in batch_indices:
        batch_x.append(Get_Features(X[index]))
        batch_y.append(Y[index])
    return batch_x, batch_y

class LinearRegression:

    def __init__(self, num_weights=201, max_iter=200, batch_size=64,
                    learning_rate=1e-3, reg_strength=1e-4, convergence_threshold=1e-4):
        self._init_weights(num_weights)
        self.max_iter = max_iter
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.reg_strength = reg_strength
        self.convergence_threshold = convergence_threshold
    
    def loss(self, X, Y):
        predictions = self.predict(X)
        error = [actual - predicted for actual, predicted in zip(Y, predictions)]
        return error

    def score(self, X, Y):
        error = []
        for x, y in zip(X, Y):
            features = Get_Features(x)
            prediction = self.predict([features])[0]
            error.append((prediction - y)**2)
        return sum(error)/float(len(error)) 
        
        
    def fit(self, X, Y, test_X, test_Y, verbose=False, log_filename="test.log"):
        self._init_weights(51)
        velocity = [0 for _ in range(51)]
        weight_delta = [0 for _ in range(51)]
        prev_error = 0
        convergence_count = 0
        for t in range(self.max_iter):
       
            batch_X, batch_Y = get_batch(X, Y, self.batch_size)

            error = self.loss(batch_X, batch_Y)
            square_error = sum([e**2 for e in error])/float(len(error))
            print "Batch Error: {}".format(square_error)
            with open(log_filename, "a") as log_file:
                log_file.write("{},{}\n".format(t,square_error))
            if abs(square_error - prev_error) < self.convergence_threshold:
                convergence_count += 1
            else:
                convergence_count = 0
            if convergence_count == 2:
                break
            prev_error = square_error            

            for i in range(len(batch_X[0])):
                weight_delta[i] = 0
                for j in range(len(batch_X)):
                    weight_delta[i] += batch_X[j][i]*error[j]
                weight_delta[i] /= float(len(batch_X))
                v_prev = velocity[i]
                velocity[i] = 0.5*velocity[i] + self.learning_rate*weight_delta[i]
                self.weights[i] += 0.5*v_prev + (1+0.5)*velocity[i]
 
            

    def predict(self, X):
        predictions = []
        for x in X:
            prediction = 0
            for feature, weight in zip(x, self.weights):
                prediction += feature*weight
            predictions.append(prediction)
        return predictions
            
    
    def _init_weights(self, num_weights):
        self.weights = [random.random()*1e-3 for _ in range(num_weights)]

    def load_weights(self, filename):
        self.weights = []
        with open(filename, "r") as weight_file:
            for weight in weight_file:
                weight = float(weight.strip())
                self.weights.append(weight)
    
    def save_weights(self, filename):
        with open(filename, "w") as weight_file:
            for weight in self.weights:
                weight_file.write("{}\n".format(weight))          
