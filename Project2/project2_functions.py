from random import sample, seed
from Tree import Node
from ID3 import ID3
from math import sqrt


def read_file(filename):
    """
    :param filename: Gets the sequences from the Proteins.fa and Proteins.sa files
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


def extract_features(sequences, labels=None):
    """
    :param sequences: list of proten sequences
    :return: return the extracted features from the sequences
    """

    print "Extracting features ..."
    feature_dict = {}
    feature_vectors = []
    new_labels = []

    if labels == None:
        labels = [[0 for _ in range(len(sequences[0]))] for _ in range(len(sequences))]

    # Create the feature vector look up table
    with open("Residue_Features.txt", "r") as feature_file:
        for line in feature_file:
            line = line.strip().split(" ")
            feature_dict[line[0]] = [int(x) for x in line[1:]]

    # Extract features from the sequences
    for sequence, label_list in zip(sequences, labels):
        sequence_features = []
        new_label = []
        for residue, label in zip(sequence, label_list):
            if residue != "X":
                sequence_features.append(feature_dict[residue])
                new_label.append(label)
        feature_vectors.append(sequence_features)
        new_labels.append(new_label)
    return feature_vectors, new_labels


def build_decision_tree(training_data_acids, training_data_labels):
    """
    Based on the training data and information gain,
    build a decision tree that can accurately predict if an amino acid
    will be exposed(e) or buried(-)
    :param training_data_acids: The amino acids in the training data set
    :param training_data_labels: The labels in the training data set
    :return: A binary tree that represents a decision tree based on the given features
    """

    print "Building tree ..."

    # Flatten the data for training
    flat_training_data_acids = []
    flat_training_data_labels = []
    for x, y in zip(training_data_acids, training_data_labels):
        flat_training_data_acids.extend(x)
        flat_training_data_labels.extend(y)

    # Build decision tree with training data
    attributes = [i for i in range(len(training_data_acids[0][0]))]
    decision_tree = ID3(attributes, flat_training_data_acids, flat_training_data_labels)

    return decision_tree


def traverse_tree(decision_tree, test_data_acids):
    """
    :param decision_tree: Decision tree built from build_decision_tree
    :param test_data_acids: Amino acids from test data set
    :return: A list of the labels generated from traversing the decision tree
    """

    print "Traversing tree ..."

    list_of_test_instance_labels = []
    test_instance_labels = []

    # iterate through amino acid sequences
    for test_instances in test_data_acids:

        # iterate through amino acid in sequences
        for test_instance in test_instances:

            # get exposed or buried prediction using decision tree, given the test instance
            test_instance_label = predict_exposed_buried(decision_tree, test_instance)

            # add the label to the inner loop labels
            test_instance_labels.append(test_instance_label)

        #print '%s' % ''.join(map(str, test_instance_labels))

        # add the inner loop labels to the final return list
        list_of_test_instance_labels.append(test_instance_labels)

        # clear the inner loops list to avoid duplicate labels
        test_instance_labels = []

    return list_of_test_instance_labels


def predict_exposed_buried(decision_tree, test_instance):
    """
    :param decision_tree: Decision tree built from build_decision_tree
    :param test_instance: Amino acids instance from test data set
    :return: either 'e' or '-' for exposed or buried, respectively
    """

    # Base case
    if decision_tree.Label is not None:
        return decision_tree.Label

    if test_instance[decision_tree.Attribute] == 1:
        # if the instance node has a '1' in the index slot for this attribute, then take the positive branch route
        next_decision_tree_node = decision_tree.Positive_Branch
    else:
        # if the instance node has a '0' in the index slot for this attribute, then take the negative branch route
        next_decision_tree_node = decision_tree.Negative_Branch

    # recurse with positive or negative branch
    return predict_exposed_buried(next_decision_tree_node, test_instance)


def evaluate(test_data, results_data):
    """
    Use Precision, Recall, Accuracy, F-1 Score, and MCC to evaluate the accuracy of the decision tree
    and print their values
    :param test_data: test data set
    :param results_data: list of the labels generated in the traverse_tree method
    :return: void
    """

    print "Evaluating results ...\n"

    fp = 0  # false positive
    fn = 0  # false negative
    tp = 0  # true positive
    tn = 0  # true negative

    index = 0
    while index < len(results_data):
        for label_index, results_label in enumerate(results_data[index]):
            test_label = test_data[index][label_index]
            if test_label == 'e':
                # positive case
                if results_label == 'e':
                    tp += 1
                else:
                    # results_data == '-'
                    fn += 1
            if test_label == '-':
                # negative case
                if results_label == '-':
                    tn += 1
                else:
                    # results_data == 'e'
                    fp += 1

        index += 1

    accuracy = (tp + tn) / float(tp + tn + fp + fn)
    print 'Accuracy: %.3f' % accuracy

    precision = tp / float(tp + fp)
    print 'Precision: %.3f' % precision

    recall = tp / float(tp + fn)
    print 'Recall: %.3f' % recall

    f1_score = (recall * precision * 2) / (recall + precision)
    print 'F1 score: %.3f' % f1_score

    # Mathews Correlation Coefficient
    mcc_num = (tp * tn) - (fp * fn)
    mcc_denom = pow(((tp + fp)*(tp + fn)*(tn + fp)*(tn + fn)), 0.5)
    mcc = mcc_num / mcc_denom
    print 'Mathews Correlation Coefficient: %.3f' % mcc