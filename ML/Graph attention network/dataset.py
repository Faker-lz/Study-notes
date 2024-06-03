import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader

class KnowledgeGraphDataset(Dataset):
    def __init__(self, triples, entity2id, relation2id):
        self.triples = triples
        self.entity2id = entity2id
        self.relation2id = relation2id

    def __len__(self):
        return len(self.triples)

    def __getitem__(self, idx):
        head, relation, tail = self.triples[idx]
        return self.entity2id[head], self.relation2id[relation], self.entity2id[tail]

def load_data(filepath):
    entity_set = set()
    relation_set = set()
    triples = []

    with open(filepath, 'r') as file:
        for line in file:
            head, relation, tail = line.strip().split('\t')
            entity_set.add(head)
            entity_set.add(tail)
            relation_set.add(relation)
            triples.append((head, relation, tail))

    entity2id = {entity: idx for idx, entity in enumerate(entity_set)}
    relation2id = {relation: idx for idx, relation in enumerate(relation_set)}

    return triples, entity2id, relation2id

def build_adjacency_matrix(triples, entity2id, relation2id):
    n_entities = len(entity2id)
    adj_matrix = np.zeros((n_entities, n_entities))

    for head, relation, tail in triples:
        head_id = entity2id[head]
        tail_id = entity2id[tail]
        adj_matrix[head_id, tail_id] = 1

    adj_matrix = torch.tensor(adj_matrix, dtype=torch.float)
    return adj_matrix

if __name__ == '__main__':
    import os 
    triples, entity2id, relation2id = load_data(os.path.join(os.path.dirname(__file__) ,r'data\WN18RR\train.txt'))
    adj_matrix = build_adjacency_matrix(triples, entity2id, relation2id)
    dataset = KnowledgeGraphDataset(triples, entity2id, relation2id)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    for data in dataloader:
        print(data)
