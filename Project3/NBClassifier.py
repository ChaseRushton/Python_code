import math

class NBClassifier:

    def calc_mean_and_variance(self, attributes):
        """
        Calculate the mean of each attribute for each label
        :param attributes: Attributes for the label
        :param prior: The prior value of a particular label
        :return: A tuple of with the list of means and the list of variances for a label
        """

        means = []
        variances = []

        # get the number of all the attribute lists we're looking at as well as the number of attributes in each list
        num_attributes_lists = len(attributes)
        num_attributes = len(attributes[0])

        # get means
        for i in range(num_attributes):
            avg = 0
            for attr in attributes:
                avg += attr[i]

            avg = float(avg) / num_attributes_lists
            means.append(avg)

        # get variances
        for i in range(num_attributes):
            avg = 0
            for attr in attributes:
                avg += (attr[i] - means[i]) ** 2

            avg = float(avg) / num_attributes_lists
            variances.append(avg)

        return means, variances

    def calc_gaussian(self, m_and_v, attr):
        """
        Calculate the probability of an attribute given a label
        :param m_and_v: means and variances for a label
        :param attr: the attributes about to be calculated
        :return: The a list of probabilities of the attribute given the label
        """
        means, variances = m_and_v
        gaussian_vals = []
        pi = 3.141

        for i in range(len(attr)):
            gauss = (1 / math.sqrt(2 * pi * variances[i])) * math.exp(-1 * ((attr[i] - means[i]) ** 2) / (2 * variances[i]))
            gaussian_vals.append(gauss)

        return gaussian_vals


    def fit(self, X, y):
        """
        Trains the data used using gaussian naive bayes and returns a dictionary of means and variances
        constructed from the training data
        :param X: Training data
        :param y: label training data
        :return: A dictionary of all the means and variances for each label
        """

        print "Calculating means and variances..."

        flat_X = []
        flat_y = []
        for seq_X, seq_y in zip(X, y):
            for a_X, a_y in zip(seq_X, seq_y):
                flat_X.append(a_X)
                flat_y.append(a_y)

        X = [flat_X]
        y = [flat_y]

        label_length = len(y[0])

        helix_count = 0
        strand_count = 0
        coil_count = 0

        # extract the attributes for each label
        helix_attributes = []
        strand_attributes = []
        coil_attributes = []
        labels = y[0]
        attributes = X[0]

        #for seq_X, seq_y in zip(X, y):

        for i in range(len(labels)):
            if labels[i] == 'H':
                helix_attributes.append(attributes[i])
                helix_count += 1
            if labels[i] == 'E':
                strand_attributes.append(attributes[i])
                strand_count += 1
            if labels[i] == 'C':
                coil_count += 1
                coil_attributes.append(attributes[i])

        helix_prior = float(helix_count) / label_length
        strand_prior = float(strand_count) / label_length
        coil_prior = float(coil_count) / label_length

        priors = {}
        priors['H'] = helix_prior
        priors['E'] = strand_prior
        priors['C'] = coil_prior

        # calculate the means for each label in training data set
        helix_means_and_variances = self.calc_mean_and_variance(helix_attributes)
        strand_means_and_variances = self.calc_mean_and_variance(strand_attributes)
        coil_means_and_variances = self.calc_mean_and_variance(coil_attributes)

        means_and_variances = {}
        means_and_variances['H'] = helix_means_and_variances
        means_and_variances['E'] = strand_means_and_variances
        means_and_variances['C'] = coil_means_and_variances

        return means_and_variances, priors



    def predict(self, X, m_and_v, priors):
        """
        Predicts the labels of the given data

        :param X: Test Data
        :param m_and_v: dictionary of the means and variances for each label constructed from the training data
        :param priors: Dictionary of priors for each label
        :return: Predicted Labels
        """

        print "Making predictions..."

        # for some reason X is a list with one element which is a list of the test data which has another list. List-ception.
        sequences = X

        predictions = []

        for sequence in sequences:
            seq_predictions = []
            for feature_vector in sequence:

                helix_gaussian = self.calc_gaussian(m_and_v['H'], feature_vector)
                strand_gaussian = self.calc_gaussian(m_and_v['E'], feature_vector)
                coil_gaussian = self.calc_gaussian(m_and_v['C'], feature_vector)

                helix_predict_attr = 1
                strand_predict_attr = 1
                coil_predict_attr = 1

                for i in range(len(helix_gaussian)):
                    helix_predict_attr *= helix_gaussian[i]
                    strand_predict_attr *= strand_gaussian[i]
                    coil_predict_attr *= coil_gaussian[i]

                helix_given_attr = helix_predict_attr * priors['H']
                strand_given_attr = strand_predict_attr * priors['E']
                coil_given_attr = coil_predict_attr * priors['C']
                all_prob = helix_given_attr + strand_given_attr + coil_given_attr

                helix_predict_label = float(helix_given_attr) / all_prob
                strand_given_label = float(strand_given_attr) / all_prob
                coil_given_label = float(coil_given_attr) / all_prob

                decision = max(helix_predict_label, strand_given_label, coil_given_label)
                #print decision

                if decision == helix_predict_label:
                    seq_predictions.append('H')
                elif decision == strand_given_label:
                    seq_predictions.append('E')
                elif decision == coil_given_label:
                    seq_predictions.append('C')
            predictions.append(seq_predictions)

        return predictions
