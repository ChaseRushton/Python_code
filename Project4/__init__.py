import Data_Utils
from LogisticRegression import LogisticRegression


if __name__ == "__main__":
    print "Loading Data ..."
    X, Y = Data_Utils.Load_Data("data/", 5)
    print "Splitting Data ..."
    train_index, test_index = Data_Utils.Split_Data(len(X))
    print "Total: {}".format(len(X))
    print "Train split: {}".format(len(train_index))
    print "Test split: {}".format(len(test_index))
    clf = LogisticRegression(batch_size=64, max_iter=200, learning_rate=1e-3, reg_strength=1e-4, convergence_threshold=1e-4)
    clf.fit(X, Y, train_index, test_index, verbose=True)
    clf.save_weights("test.mdl")
