'''
Author: WLZ
Date: 2024-06-03 21:11:37
Description: 
'''
import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import DataLoader
from graphAttentionNetwork import MultiLayerGAT
from dataset import KnowledgeGraphDataset, load_data, build_adjacency_matrix


class KnowledgeGraphTrainer:
    def __init__(self, all_file_path, train_file_path, valid_file_path, entity_dim, relation_dim, dropout, 
                 alpha, nheads, batch_size=32, lr=0.01, num_epochs=10):
        self.all_file_path = all_file_path
        self.train_file_path = train_file_path
        self.valid_file_path = valid_file_path
        self.entity_dim = entity_dim
        self.relation_dim = relation_dim
        self.dropout = dropout
        self.alpha = alpha
        self.nheads = nheads
        self.batch_size = batch_size
        self.lr = lr
        self.num_epochs = num_epochs    

        all_entity2id, all_relation2id = load_data(all_file_path, True)
        self.train_dataset = KnowledgeGraphDataset(train_file_path, all_entity2id, all_relation2id)
        self.valid_dataset = KnowledgeGraphDataset(valid_file_path, all_entity2id, all_relation2id)
        self.train_dataloader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=True)
        self.valid_dataloader = DataLoader(self.valid_dataset, batch_size=batch_size, shuffle=True)
        self.adj_matrix = build_adjacency_matrix(self.train_dataset.triples, self.train_dataset.entity2id)
        
        self.n_entities = len(self.entity2id)
        
        self.model = MultiLayerGAT(entity_dim, entity_dim, entity_dim, dropout, alpha, nheads)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.BCEWithLogitsLoss()
        
        self.entity_embeddings = nn.Embedding(self.n_entities, entity_dim)
        nn.init.xavier_uniform_(self.entity_embeddings.weight)
        
    def train(self):
        self.model.train()
        for epoch in range(self.num_epochs):
            total_loss = 0
            for batch in self.dataloader:
                head, relation, tail = batch
                head = head.to(torch.long)
                tail = tail.to(torch.long)

                self.optimizer.zero_grad()

                x = self.entity_embeddings.weight
                output = self.model(x, self.adj_matrix)
                
                head_emb = output[head]
                tail_emb = output[tail]

                score = torch.sum(head_emb * tail_emb, dim=1)
                target = torch.ones_like(score)

                loss = self.criterion(score, target)
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()

            print(f'Epoch {epoch+1}, Loss: {total_loss/len(self.dataloader)}')