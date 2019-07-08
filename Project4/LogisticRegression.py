import random
import math
from Data_Utils import Get_Data

def sigmoid_forward(x):
    return 1/(1+math.exp(-x))

def sigmoid_backward(x):
    return x*(1-x)

def _get_batches(X, Y, batch_size=32):
    data_combined = list(zip(X, Y))
    random.shuffle(data_combined)
    for i in range(0, len(X), batch_size):
        batch = data_combined[i:i+batch_size]
        batch_x, batch_y = zip(*batch)
        yield batch_x, batch_y
        
def get_batch(X, Y, batch_size=32):
    batch_indices = random.sample(range(len(X)), batch_size)
    batch_x = []
    batch_y = []
    index_counter = 0
    for index in batch_indices:
        batch_x.append(X[index])
        batch_y.append(Y[index])
    return batch_x, batch_y

def get_batch_index(indices, batch_size=32):
    batch_index = random.sample(indices, batch_size)
    return batch_index

class LogisticRegression:

    def __init__(self, num_weights=201, max_iter=200, batch_size=64,
                    learning_rate=1e-3, reg_strength=1e-4, convergence_threshold=1e-4):
        self._init_weights(num_weights)
        self.max_iter = max_iter
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.reg_strength = reg_strength
        self.convergence_threshold = convergence_threshold
    
    def loss(self, X, Y):
        probs = self.predict(X)
        error = [a - p for a, p in zip(Y, probs)]
        grads = [sigmoid_backward(x) for x in probs]
        return error, grads
        
        
    def fit(self, X, Y, train_index, test_index, verbose=False, log_filename="test.log"):
        self._init_weights(len(X[0]))
        acc_train_error = 0
        acc_test_error = 0
        for t in range(self.max_iter):
            if verbose and t % 5 == 0 and t != 0:
                avg_train_error = acc_train_error/(self.batch_size*5.0)
                avg_test_error = acc_test_error/(self.batch_size*5.0)
                acc_train_error = 0
                acc_test_error = 0
                print "Train Error: {}".format(avg_train_error)
                print "Test Error: {}\n".format(avg_test_error)
                with open(log_filename, "a") as log_file:
                    log_file.write("{},{},{}\n".format(t,avg_train_error, avg_test_error))

            batch_index = get_batch_index(train_index, self.batch_size)
            test_batch_index = get_batch_index(test_index, self.batch_size)

            batch_X, batch_Y = Get_Data(X, Y, batch_index)
            test_batch_X, test_batch_Y = Get_Data(X, Y, test_batch_index)

            error, grads = self.loss(batch_X, batch_Y)
            test_error, _ = self.loss(test_batch_X, test_batch_Y)

            acc_train_error += sum([e**2 for e in error])
            acc_test_error += sum([e**2 for e in test_error])

            weight_delta = [e*g for e, g in zip(error,grads)]
            weight_update = [0 for _ in range(len(batch_X[0]))]
            
            for i in range(len(batch_X[0])):
                for j in range(len(batch_X)):
                    weight_update[i] += batch_X[j][i]*weight_delta[j]
                self.weights[i] += self.learning_rate*(- self.reg_strength*self.weights[i] + weight_update[i]/float(len(batch_X)))

        if verbose:
            avg_train_error = acc_train_error/(self.batch_size*5.0)
            avg_test_error = acc_test_error/(self.batch_size*5.0)
            acc_train_error = 0
            acc_test_error = 0
            print "Train Error: {}".format(avg_train_error)
            print "Test Error: {}\n".format(avg_test_error)
            with open(log_filename, "a") as log_file:
                log_file.write("{},{},{}\n".format(t,avg_train_error, avg_test_error))

                 
            

    def predict(self, X):
        predictions = []
        for x in X:
            prediction = 0
            for feature, weight in zip(x, self.weights):
                prediction += feature*weight
            predictions.append(sigmoid_forward(prediction))
        return predictions
            
    
    def _init_weights(self, num_weights):
        self.weights = [random.random()*1e-3 for _ in range(num_weights)]
    
    def save_weights(self, filename):
        with open(filename, "w") as weight_file:
            for weight in self.weights:
                weight_file.write("{}\n".format(weight))          
