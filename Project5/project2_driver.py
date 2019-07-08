import project2_functions as p2f
import sys
from ID3 import Serialize_Tree, Deserialize_Tree

if len(sys.argv) < 3:
    print "usage: python project2_driver.py sequences_file_name labels_file_name model_filename\n"
    print "usage: python project2_driver.py sequences_file_name model_filename"
    sys.exit()

if len(sys.argv) == 4:
    
    amino_acids = p2f.read_file(sys.argv[1])
    amino_labels = p2f.read_file(sys.argv[2])
    amino_acids, amino_labels = p2f.extract_features(amino_acids, amino_labels)
    acid_train, acid_test, label_train, label_test = p2f.split_data(amino_acids, amino_labels)

    decision_tree = p2f.build_decision_tree(acid_train, label_train)

    Serialize_Tree(decision_tree, sys.argv[3])
    result_sequence = p2f.traverse_tree(decision_tree, acid_test)

    p2f.evaluate(label_test, result_sequence)

if len(sys.argv) == 3:
    
    amino_acids = p2f.read_file(sys.argv[1])
    amino_acids, _ = p2f.extract_features(amino_acids)
    s_tree = Deserialize_Tree(sys.argv[2])

    result_sequence = p2f.traverse_tree(s_tree, amino_acids)
    print("\n".join(["".join([j for j in x]) for x in result_sequence]))