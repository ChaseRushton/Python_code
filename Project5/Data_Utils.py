import os
import random
import sys
import Blast_Utils
import External_Feature_Extraction as efe
import project3_functions
from NBClassifier import NBClassifier

def Load_Dataset(data_filename):
    X = []
    Y = []
    with open(data_filename, "r") as data_file:
        for line in data_file:
            line = line.strip().split(",")
            X.append((line[0], line[1]))
            Y.append(float(line[2]))
    return X, Y

def Split_Data(X, Y, test_split=.25):
    train_x = []
    test_x = []
    train_y = []
    test_y = []
    test_indices = random.sample(range(len(X)), int(len(X)*test_split))
    for i in range(len(X)):
        if i in test_indices:
            test_x.append(X[i])
            test_y.append(Y[i])
        else:
            train_x.append(X[i])
            train_y.append(Y[i])
    return train_x, test_x, train_y, test_y

def Get_Features(X):

    clf = NBClassifier()

    seq1, seq2 = X
    gnb1_pssm, lr1 = Blast_Utils.Get_PSSM(seq1 + ".pssm")
    gnb2_pssm, lr2 = Blast_Utils.Get_PSSM(seq2 + ".pssm")

    means_and_variances, priors = project3_functions.load_model("800_sequence_model.mdl")
    gnb_predictions1 = clf.predict(gnb1_pssm, means_and_variances, priors)
    gnb_predictions2 = clf.predict(gnb2_pssm, means_and_variances, priors)

    gnb1_features = efe.Extract_GNB_Features(gnb_predictions1)
    gnb2_features = efe.Extract_GNB_Features(gnb_predictions2)
 
    dt1 = efe.Extract_Decision_Tree_Features(seq1 + ".fasta")
    dt2 = efe.Extract_Decision_Tree_Features(seq2 + ".fasta")

    lr1.extend(lr2)
    lr1.extend(gnb1_features)
    lr1.extend(gnb2_features)
    lr1.extend(dt1)
    lr1.extend(dt2)
    lr1.append(1)
    return lr1

