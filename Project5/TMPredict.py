import sys
from LinearRegression import LinearRegression
from Data_Utils import Get_Features

if __name__ == "__main__":
    seq1_fileextension = sys.argv[1].split(".")[-1]
    seq2_fileextension = sys.argv[2].split(".")[-1]
    seq1_filename = sys.argv[1][:-len(seq1_fileextension) - 1]
    seq2_filename = sys.argv[2][:-len(seq2_fileextension) - 1]

    features = Get_Features((seq1_filename, seq2_filename))
    
    clf =  LinearRegression()
    clf.load_weights("lr.mdl")
    print(clf.predict([features]))
