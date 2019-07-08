import project2_functions as p2f
import sys
from ID3 import Deserialize_Tree


def Extract_Decision_Tree_Features(fasta_file):
    amino_acids = p2f.read_file(fasta_file)
    amino_acids, _ = p2f.extract_features(amino_acids)

    s_tree = Deserialize_Tree("Decision_Tree")

    result_sequence = p2f.traverse_tree(s_tree, amino_acids)

    exposed_count = 0
    buried_count = 0
    for i in result_sequence[0]:
        if i == 'e':
            exposed_count += 1
        else:
            buried_count += 1

    result_length = len(result_sequence[0])
    exposed_percent = float(exposed_count) / result_length
    buried_percent = float(buried_count) / result_length

    project2_features = [exposed_percent, buried_percent]

    return project2_features



def Extract_GNB_Features(prediction):
    pred = prediction[0]
    prediction_length = len(pred)

    h_count = 0
    e_count = 0
    c_count = 0

    for result in pred:
        if result == 'H':
            h_count += 1
        elif result == 'C':
            c_count += 1
        elif result == 'E':
            e_count += 1

    h_prob = float(h_count) / prediction_length
    e_prob = float(e_count) / prediction_length
    c_prob = float(c_count) / prediction_length

    gnb_features = [h_prob, e_prob, c_prob]

    return gnb_features


