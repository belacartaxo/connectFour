from collections import Counter
import numpy as np
from NodeDT import NodeDT

class DecisionTree:
    def __init__(self, min_sample_split=2, max_depth=15, n_features=None) -> None:
        """
        Initializes the Decision Tree classifier.

        Parameters:
        - min_sample_split: Minimum number of samples required to split an internal node.
        - max_depth: Maximum depth allowed for the tree.
        - n_features: Number of features to consider when looking for the best split.
        """
        self.min_sample_split = min_sample_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.root = None

    def fit(self, X, y):
        """
        Fits the Decision Tree to the training data by building the tree recursively.
        """
        self.n_features = X.shape[1]
        self.root = self.grow_tree(X, y)

    def grow_tree(self, X, y, depth=0):
        """
        Recursively builds the decision tree.
        """
        n_samples, n_feats = X.shape
        n_labels = len(np.unique(y))

        # Stopping conditions
        if (depth >= self.max_depth or n_labels == 1 or n_samples < self.min_sample_split):
            leaf_value = self.most_common_label(y)
            return NodeDT(value=leaf_value)

        best_feature, best_value = self.best_split(X, y, list(range(n_feats)))

        node = NodeDT(feature=best_feature)

        for value in np.unique(X.iloc[:, best_feature]):
            idxs = self.split(X.iloc[:, best_feature], value)
            if len(idxs) > 0:
                node.children[value] = self.grow_tree(
                    X.iloc[idxs, :],
                    y.iloc[idxs],
                    depth + 1
                )

        return node

    def most_common_label(self, y):
        """
        Returns the most common label in the target array y.
        """
        counter = Counter(y)
        value = counter.most_common(1)
        if value:
            return value[0][0]
        return value

    def best_split(self, X, y, feat_idxs):
        """
        Finds the feature and value that provide the best information gain.
        """
        if feat_idxs is None:
            feat_idxs = range(X.shape[1])

        best_gain = -1
        best_split_feat, best_split_value = None, None

        for feat_idx in feat_idxs:
            X_column = X.iloc[:, feat_idx]
            limits = np.unique(X_column)

            for split_criteria in limits:
                gain = self.information_gain(y, X_column, split_criteria)

                if gain > best_gain:
                    best_gain = gain
                    best_split_feat = feat_idx
                    best_split_value = split_criteria

        return best_split_feat, best_split_value

    def information_gain(self, y, X_column, split_criteria):
        """
        Computes the information gain of a split.
        """
        parent_entropy = self.entropy(y)
        matching_idxs = self.split(X_column, split_criteria)
        non_matching_idxs = np.setdiff1d(np.arange(len(X_column)), matching_idxs)

        if len(matching_idxs) == 0 or len(non_matching_idxs) == 0:
            return 0

        n = len(y)
        n_matching = len(matching_idxs)
        n_non_matching = len(non_matching_idxs)

        e_matching = self.entropy(y.iloc[matching_idxs])
        e_non_matching = self.entropy(y.iloc[non_matching_idxs])

        child_entropy = (n_matching / n) * e_matching + (n_non_matching / n) * e_non_matching

        information_gain = parent_entropy - child_entropy

        return max(0, information_gain)

    def split(self, X_column, value):
        """
        Returns the indices of samples where the feature matches the given value (categorical split).
        """
        matching_idxs = np.argwhere(X_column == value).flatten()
        return matching_idxs

    def entropy(self, y):
        """
        Computes the entropy of the target labels.
        """
        counts = np.bincount(y)
        ps = counts / len(y)
        return -np.sum([p * np.log2(p) for p in ps if p > 0])

    def predict(self, X):
        """
        Predicts the class labels for the input data X.
        """
        return list(self.traverse_tree(x, self.root) for x in X.values)

    def traverse_tree(self, x, node):
        """
        Recursively traverses the tree to make a prediction for a single sample.
        """
        if node.is_leaf():
            return node.value

        if x[node.feature] in node.children:
            return self.traverse_tree(x, node.children[x[node.feature]])

        return node.value  # fallback if branch is missing


def accuracy(y_test, y_pred):
    """
    Calculates the accuracy of predictions.
    """
    return np.mean(y_test == y_pred) * 100
