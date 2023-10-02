"""
Framework for graph classification
"""

import torch.nn as nn
from torch_geometric.nn import global_add_pool, global_mean_pool, global_max_pool, AttentionalAggregation
from torch.nn import BatchNorm1d as BN
import torch.nn.functional as F


class GraphClassification(nn.Module):
    def __init__(self, embedding_model, pooling_method, output_size):
        """framework for graph classification
        Args:
            embedding_model (nn.Module):  graph neural network embedding model
            pooling_method (str): graph pooling method
            output_size (int): output size, equal to the number of class for classification
        """
        super(GraphClassification, self).__init__()
        self.embedding_model = embedding_model
        hidden_size = embedding_model.hidden_size
        self.JK = self.embedding_model.JK
        self.num_layer = self.embedding_model.num_layer
        self.pooling_method = pooling_method

        # Different kind of graph pooling
        if pooling_method == "sum":
            self.pool = global_add_pool
        elif pooling_method == "mean":
            self.pool = global_mean_pool
        elif pooling_method == "max":
            self.pool = global_max_pool
        elif pooling_method == "attention":
            self.pool = AttentionalAggregation(gate_nn=nn.Linear(hidden_size, 1))
        else:
            raise ValueError("The pooling method not implemented")

        # classifier
        self.classifier = nn.Linear(hidden_size, output_size)
        # self.classifier_1 = nn.Linear(hidden_size, hidden_size)
        # self.classifier_2 = nn.Linear(hidden_size, output_size) 
        self.bn = BN(num_features=output_size, momentum=1.0, affine=False)

        self.reset_parameters()

    def reset_parameters(self):
        self.embedding_model.reset_parameters()
        self.classifier.reset_parameters()
        # self.classifier_1.reset_parameters()
        # self.classifier_2.reset_parameters()
        if self.pooling_method == "attention":
            self.pool.reset_parameters()
        self.bn.reset_parameters()

    def forward(self, data):
        batch = data.batch
        # node representation
        x = self.embedding_model(data)
        pool_x = self.pool(x, batch)
        # return self.classifier(pool_x)
        return self.bn(self.classifier(pool_x))
        # return self.classifier_2(F.relu(self.bn(self.classifier_1(pool_x))))
