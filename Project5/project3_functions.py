from random import sample, seed
from math import sqrt

def read_file(filename):
    """
    :param filename: Gets the sequences from the Proteins.fa and Proteins.ss files
    :return: A list of sequences of amino acids and their results in the files
    """
    Data = []
    print "reading file {} ...".format(filename)
    with open(filename, "r") as data_file:
        for line in data_file:
            line = line.strip()
            if len(line) == 0:
                continue
            if ">" not in line: 
                Data.append(list(line))

    return Data


def split_data(acids, labels):
    """
    Split the data from the Proteins.sa/.fa files into training set data and test data.
    Training set data: ~75% of the total data
    Test set data: ~25% of the total data
    Make sure the two sets aren't overlapping and that the data is selected randomly without replacement
    
    :param acids: List of the acids from the Proteins.fa file
    :param labels: List of the labels from the Proteins.sa file in respect to the Proteins.fa file
    :return: A tuple containing the training set of data and the test data in the form (acid_train, acid_test,
    label_train, label_test)
    """
    print "Calculating splits ..."
    # Initialize data
    seed(0)
    acid_train = []
    acid_test = []
    label_train = []
    label_test = []
    num_total = len(acids)

    # Determine test set indices
    test_indicies = sample(range(num_total), int(num_total*.25))

    # Split the data based on test indices
    for i in range(num_total):
        # Add to test set
        if i in test_indicies:
            acid_test.append(acids[i])
            label_test.append(labels[i])
        # Add to training set
        else:
            acid_train.append(acids[i])
            label_train.append(labels[i])

    return acid_train, acid_test, label_train, label_test

def evaluate(predictions, y):
    """
    Calculate Q3 Accuracy

    :param predictions: Predicted Labels
    :param y: Acutal Labels
    :return: Q3 Accuracy
    """

    print "Evaluating results ...\n"

    correct = 0.0
    num_total = float(len(y))

    for pred_seq, actual_seq in zip(predictions, y):
        for pred_label, actual_label in zip(pred_seq, actual_seq):
            if pred_label == actual_label:
                correct += 1.0
    return correct/num_total

def save_model(means_and_variances, priors, filename):
    with open(filename, "w") as model_file:
        for label in means_and_variances:
            model_file.write("{},{},{},{}\n".format(label, priors[label], ",".join([str(x) for x in means_and_variances[label][0]]), ",".join([str(x) for x in means_and_variances[label][1]])))

def load_model(filename):
    mean_and_vars = {}
    priors = {}
    with open(filename, "r") as model_file:
        for line in model_file:
            line = line.strip().split(",")
            label = line[0]
            prior = line[1]
            means = [float(x) for x in line[2:int((len(line))/2)+1]]
            vars = [float(x) for x in line[int((len(line))/2)+1:]]
            mean_and_vars[label] = [means, vars]
            priors[label] = float(prior)
    return mean_and_vars, priors


    
