import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import DataLoader
from graphAttentionNetwork import MultiLayerGAT
from dataset import KnowledgeGraphDataset, load_data, build_adjacency_matrix


class KnowledgeGraphTrainer:
    def __init__(self, filepath, entity_dim, relation_dim, dropout, alpha, nheads, batch_size=32, lr=0.01, num_epochs=10):
        self.filepath = filepath
        self.entity_dim = entity_dim
        self.relation_dim = relation_dim
        self.dropout = dropout
        self.alpha = alpha
        self.nheads = nheads
        self.batch_size = batch_size
        self.lr = lr
        self.num_epochs = num_epochs
        
        self.triples, self.entity2id, self.relation2id = load_data(filepath)
        self.dataset = KnowledgeGraphDataset(self.triples, self.entity2id, self.relation2id)
        self.dataloader = DataLoader(self.dataset, batch_size=batch_size, shuffle=True)
        self.adj_matrix = build_adjacency_matrix(self.triples, self.entity2id)
        
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