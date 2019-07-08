class Node:
    """
    Args:
        attribute (int): Index of the attribute to be test. (None if this is a leaf node)
        label (int): Label of leaf node. (None if this is a decision node)

    Attributes:
        Attribute (int): Index of the attribute to be test. (None if this is a leaf node)
        Label (int): Label of leaf node. (None if this is a decision node)
        Positive_Branch (Node): The branch taken if the instance's attribute being tested is positive.
        Negative_Branch (Node): The branch taken if the instance's attribute being tested is negative.

    """
    def __init__(self, attribute=None, label=None):
        self.Attribute = attribute
        self.Label = label
        self.Positive_Branch = None
        self.Negative_Branch = None

        