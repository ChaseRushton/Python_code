from Tree import Node
import math
import random

def ID3(Attributes, X, Y):
    """
    Implementaion of the ID3 Algorithm

    :param Attributes: List of attributes to test
    :param X: set of training instances
    :param Y: set of training labels
    :return: decision tree build from the training data
    """
    # Handle base cases
    num_positive, num_negative = Calculate_Counts(Y)
    # All labels are positive
    if num_positive == len(Y):
        return Node(label='e')
    # All labels are negative
    elif num_negative == len(Y):
        return Node(label='-')
    # No attributes left to test (Choose the most common label amongst the remaining examples)
    if len(Attributes) == 0:
        if num_positive > num_negative:
            return Node(label='e')
        elif num_positive < num_negative:
            return Node(label='-')
        else:
            return Node(label=random.choice(['e','-']))

    # Determine the best attribute
    max_gain = None
    max_attribute = 0
    max_indices = []
    positive_splits = []
    negative_splits = []
    gains = []
    for i in range(len(Attributes)):
        gain, positive_split, negative_split = Gain(Attributes[i], X, Y)
        gains.append(gain)
        positive_splits.append(positive_split)
        negative_splits.append(negative_split)
        # Keep track of max gain(s)
        if max_gain == None:
            max_gain = gain
            max_indices.append(i)
        elif gain > max_gain:
            max_gain = gain
            max_indices = [i]
        elif gain == max_gain:
            max_indices.append(i)
        

    max_index = random.choice(max_indices)
    max_attribute = Attributes[max_index]
    max_positive_split = positive_splits[max_index]
    max_negative_split = negative_splits[max_index]

    # Remove the attribute from the list of attributes (Attrubutes - {A})
    Attributes = Attributes[:max_index] + Attributes[max_index+1:]

    # Set Attribute of the decision node to the one with the max gain
    current_node = Node(attribute=max_attribute)

    # Build positive child node
    if len(max_positive_split[0]) > 0:
        current_node.Positive_Branch = ID3(Attributes, max_positive_split[0], max_positive_split[1])
    else:
        if num_positive > num_negative:
            current_node.Positive_Branch = Node(label='e')
        elif num_positive < num_negative:
            current_node.Positive_Branch = Node(label='-')
        else:
            current_node.Positive_Branch = Node(label=random.choice(['e','-']))

    # Build negative child node
    if len(max_negative_split[0]) > 0:
        current_node.Negative_Branch = ID3(Attributes, max_negative_split[0], max_negative_split[1])
    else:
        if num_positive > num_negative:
            current_node.Negative_Branch = Node(label='e')
        elif num_positive < num_negative:
            current_node.Negative_Branch = Node(label='-')
        else:
            current_node.Negative_Branch = Node(label=random.choice(['e','-']))
    return current_node

def H(proportion_pos):
    """
    Calculates entropy based on the given proportions

    :param proportion_pos: Proportion of positive training examples
    :return: Returns the entropy based on the given proportion
    """
    if proportion_pos == 0 or proportion_pos == 1:
        return 0
    return -(proportion_pos*math.log(proportion_pos, 2)) - ((1-proportion_pos)*math.log((1-proportion_pos), 2))

def Attribute_Split(Attribute, X, Y):
    """
    Splits the data on the given attribute and calculates the proportion 
    of positive lables in the total set and both of the splits which is 
    used later for calculating the entropy and information gain of these sets

    :param Attribute: Attribute to perform split on
    :param X: List of training instances
    :param Y: List of training labels
    :return: Two splits based on the given attribute along with proportions of positive examples
                ((pos_X, pos_Y, proportion_pos), (neg_X, neg_Y, proportion_pos), total_proportion_pos)
    """
    # Initialize variables
    positive_X = []
    negative_X = []
    positive_Y = []
    negative_Y = []
    split1_num_pos = 0
    split1_num_total = 0
    split2_num_pos = 0
    split2_num_total = 0

    for i in range(len(X)):
        # The attribute is positive so place it in the positive split
        if X[i][Attribute] == 1:
            positive_X.append(X[i])
            positive_Y.append(Y[i])
            # Calculating the proportion positive in the positive attribute split
            if Y[i] == 'e':
                split1_num_pos += 1
            split1_num_total += 1
        # The attribute is negative so place it in the negative split
        else:
            negative_X.append(X[i])
            negative_Y.append(Y[i])
            # Calculating the proportion positive in the negative attribute split
            if Y[i] == 'e':
                split2_num_pos += 1
            split2_num_total += 1

    # Calculate the proportions
    split1_proportion_pos = 0
    split2_proportion_pos = 0
    total_proportion_pos = 0
    denom = 0

    # Proportion positive for each of the splits
    if split1_num_total > 0:
        split1_proportion_pos = split1_num_pos/float(split1_num_total)
        denom += split1_num_total
    if split2_num_total > 0:
        split2_proportion_pos = split2_num_pos/float(split2_num_total)
        denom += split2_num_total
    # Proportion positive for all of the instances
    if denom > 0:
        total_proportion_pos = (split1_num_pos + split2_num_pos)/float(denom)
    
    return (positive_X, positive_Y, split1_proportion_pos), (negative_X, negative_Y, split2_proportion_pos), total_proportion_pos

def Gain(Attribute, X, Y):
    """
    Calculates the information gain for the given attribute

    :param Attribute: Attribute to test
    :param X: List of training instances
    :param Y: List of training labels
    :return: Information gain for the given attribute
    """
    # Get splits and proportions
    pos_split, neg_split, proportion_pos = Attribute_Split(Attribute, X, Y)

    # Calculate weights based on split proportions
    num_pos_examples = len(pos_split[0])
    num_neg_examples = len(neg_split[0])
    num_total_examples = float(num_pos_examples + num_neg_examples)
    pos_split_weight = num_pos_examples/num_total_examples
    neg_split_weight = num_neg_examples/num_total_examples

    # Finally calculate the gain
    gain = H(proportion_pos) - (pos_split_weight*H(pos_split[2]) + neg_split_weight*H(neg_split[2]))
    
    return gain, pos_split, neg_split

def Calculate_Counts(Y):
    """
    Calculate the number of positive and negative labels

    :param Y:  List of labels
    :return: Counts of positive and negative labels
    """
    num_positive = 0
    num_negative = 0
    for label in Y:
        if label == "e":
            num_positive += 1
        else:
            num_negative += 1
    return num_positive, num_negative

def Serialize_Tree(T, file_name="Tree.model"):
    Q = []
    Q.append((0,T))
    node_id = 0
    with open(file_name, "w") as output_file:
        output_file.write("{},{},{},{},{}\n".format(0,T.Attribute,T.Label,0,"+"))
        while len(Q) > 0:
            parent_id, current_node = Q.pop()
            if current_node.Attribute is not None:
                positive_child_id = node_id + 1
                negative_child_id = node_id + 2
                Q.append((positive_child_id,current_node.Positive_Branch))
                Q.append((negative_child_id,current_node.Negative_Branch))
                output_file.write("{},{},{},{},{}\n".format(positive_child_id,current_node.Positive_Branch.Attribute,current_node.Positive_Branch.Label,parent_id,"+"))
                output_file.write("{},{},{},{},{}\n".format(negative_child_id,current_node.Negative_Branch.Attribute,current_node.Negative_Branch.Label,parent_id,"-"))
                node_id += 2

def Deserialize_Tree(file_name="Tree.model"):
    nodes = {}
    num_nodes = 0
    with open(file_name, "r") as input_file:
        for line in input_file:
            line = line.strip().split(",")
            node_id, attribute, label, parent_id, parity = line
            node_id = int(node_id)
            parent_id = int(parent_id)
            if attribute != "None":
                attribute = int(attribute)
            else:
                attribute = None
            if label == "None":
                label = None
            nodes[node_id] = [Node(attribute,label),parent_id,parity]
            num_nodes += 1
    for i in range(1,num_nodes):
        if nodes[i][2] is "+":
            nodes[nodes[i][1]][0].Positive_Branch = nodes[i][0]
        else:
            nodes[nodes[i][1]][0].Negative_Branch = nodes[i][0]
    return nodes[0][0]
