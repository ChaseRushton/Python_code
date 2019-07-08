import Blast_Utils
import External_Feature_Extraction as efe
from NBClassifier import NBClassifier
import project3_functions


def Get_Features(X):

    clf = NBClassifier()

    seq1, seq2 = X
    gnb1_pssm, lr1 = Blast_Utils.Get_PSSM(seq1 + ".pssm")
    # gnb2_pssm, lr2 = Blast_Utils.Get_PSSM(seq2 + ".pssm")

    means_and_variances, priors = project3_functions.load_model("800_sequence_model.mdl")
    gnb_predictions1 = clf.predict(gnb1_pssm, means_and_variances, priors)
    # gnb_predictions2 = clf.predict(gnb2_pssm, means_and_variances, priors)

    gnb1_features = efe.Extract_GNB_Features(gnb_predictions1)

    print gnb1_features
    # gnb2_features = efe.Extract_GNB_Features(gnb_predictions2)

    # dt1 = efe.Extract_Decision_Tree_Features(seq1 + ".fasta")
    # dt2 = efe.Extract_Decision_Tree_Features(seq2 + ".fasta")
    # lr1.extend(lr2)
    # #lr1.extend(dt1)
    # #lr1.extend(dt2)
    # lr1.append(1)
    # return lr1

x = "test", ""

Get_Features(x)


