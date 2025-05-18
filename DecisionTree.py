import pandas as pd
import numpy as np
from collections import Counter


class Node_DT:

    def __init__(self, feature = None, split_criteria = None, left = None, right = None, value=None):
        self.feature = feature                      # Ex.: numero de quartos
        self.split_criteria = split_criteria        # Ex.: <= 5 do lado esquerdo; > 5 do lado direito ==> split_criteria = 5
        self.left = left                            # nó da esquerda
        self.right = right                          # nó da direita
        self.value = value                          # caso seja uma folha, qual o valor
        self.children = {}  # Dictionary to store multiple branches

    # metodo para avaliar se é uma folha não
    def is_leaf(self) -> bool:
        return self.value is not None
    

class DecisinoTree:

    def __init__(self, min_sample_split=2, max_depth= 10, n_features=None) -> None:
        self.min_sample_split = min_sample_split    # Mínimo de amostras necessário para dividir um nó.
        self.max_depth = max_depth                  # Profundidade máxima da árvore.
        self.n_features = n_features                # Número de características usadas para realizar os splits.
        self.root = None
        
    def fit(self, X, y):
        self.n_features = X.shape[1]
        self.root = self.grow_tree(X, y)

    def grow_tree(self, X, y, depth=0):
        n_samples, n_feats = X.shape
        n_labels = len(np.unique(y))
        
        if (depth >= self.max_depth or n_labels == 1 or n_samples < self.min_sample_split):
            leaf_value = self.most_common_label(y)
            return Node_DT(value=leaf_value)
        
        best_feature, best_value = self.best_split(X, y, list(range(n_feats)))
        
        # Create node with best feature
        node = Node_DT(feature=best_feature)
        
        # For each unique value in the feature
        for value in np.unique(X.iloc[:, best_feature]):
            # Get indices for this value
            idxs = self.split(X.iloc[:, best_feature], value)
            if len(idxs) > 0:
                # Recursively grow subtree
                node.children[value] = self.grow_tree(
                    X.iloc[idxs, :], 
                    y.iloc[idxs], 
                    depth + 1
                )
        
        return node


    def most_common_label(self, y):
        counter = Counter(y)
        value = counter.most_common(1)
        if value:
            return value[0][0]
        return value

    # This is fine 
    def best_split(self, X, y, feat_idxs): # $
        if feat_idxs is None:
            feat_idxs = range(X.shape[1])
        best_gain = -1
        best_split_feat, best_split_value = None, None

        for feat_idx in feat_idxs:
            X_column = X.iloc[:, feat_idx]              # Selects all the rows with the spesified index, ou seja, this returns a series
            limits = np.unique(X_column)                # A list of [. X O ]

            for split_criteria in limits:               # split_criteria = . or x or o
                # calculate the information gain
                gain = self.information_gain(y, X_column, split_criteria)

                if gain > best_gain:
                    best_gain = gain
                    best_split_feat = feat_idx
                    best_split_value = split_criteria

        return best_split_feat, best_split_value



    def information_gain(self, y, X_column, split_criteria):
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

        child_entropy = (n_matching/n) * e_matching + (n_non_matching/n) * e_non_matching

        information_gain = parent_entropy - child_entropy

        return max(0, information_gain)


    def split(self, X_column, value):
        # For categorical data, we want exact matches
        matching_idxs = np.argwhere(X_column == value).flatten()
        return matching_idxs


    # Entropy look correct 
    def entropy(self, y): # $
        counts = np.bincount(y)
        ps = counts / len(y) 
        return - np.sum([p * np.log2(p) for p in ps if p > 0])


    def predict(self, X):
        return list(self.traverse_tree(x, self.root) for x in X.values)


    def traverse_tree(self, x, node):
        if node.is_leaf():
            return node.value
        
        if x[node.feature] in node.children:
            return self.traverse_tree(x, node.children[x[node.feature]])
        return node.value
    


def accuracy(y_test, y_pred):
    return np.mean(y_test == y_pred) * 100





df = pd.read_csv("Connect4-dataset.csv")

# optinal shuffle for randomness

x = df.drop("Best_Move", axis=1)
y = df["Best_Move"]

#cell_mapping = {'.': 0, 'O': 1, 'X': 2}


#x = x.applymap(lambda val : cell_mapping[val])     

# get the dataset dimensions
number_of_rows = df.shape[0]
number_of_cols = df.shape[1]


cutoff = int(0.8 * number_of_rows)

# Training set
X_train = x.iloc[:cutoff, :]
Y_train = y.iloc[:cutoff]

# Testing set
X_test = x.iloc[cutoff:, :]
Y_test = y.iloc[cutoff:]




tree = DecisinoTree()
tree.fit(X_train, Y_train)
prediction = tree.predict(X_test)

acc = accuracy(Y_test, prediction)

print("")
print(f"Model accuracy: {round(acc, 2)}%")
print("")


