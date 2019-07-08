import os
import random
import sys

def Load_Data(feature_dir, num_read=10):
    X = []
    y = []
    num_sequences = 0
    for file in os.listdir(feature_dir):
        if ".features" not in file:
            continue
        if num_sequences > num_read:
            break
            #pass
        with open(feature_dir + file, "r") as feature_file:
            for line in feature_file:
                line = line.strip().split(",")
                label = float(line[0])
                features = [int(x) for x in line[1:]]
                features.append(1)
                y.append(label)
                X.append(features)
        num_sequences += 1
    return X, y

def Split_Data(num_instances, test_split=.25):
    train_indices = []
    test_indices = []
    num_test = int(num_instances*.25)
    indices = [i for i in range(num_instances)]
    random.shuffle(indices)
    test_indices = indices[:num_test]
    train_indices = indices[num_test:]
    return train_indices, test_indices

def Get_Data(X, Y, indices):
    x = []
    y = []
    for i in indices:
        x.append(X[i])
        y.append(Y[i])
    return x, y
                
