'''
Author: WLZ
Date: 2024-06-03 21:05:26
Description: 
'''
import os 
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader


class KnowledgeGraphDataset(Dataset):
    def __init__(self, filepath, all_entity2id, all_relation2id):
        self.triples = load_data(filepath)
        self.entity2id = self._get_entity_id(all_entity2id)
        self.relation2id = all_relation2id
    
    def _get_entity_id(self, all_entity2id):
        entity_set = set()
        for head, _ , tail in self.triples:
            entity_set.add(head)
            entity_set.add(tail)
        entity2id = {entity: all_entity2id[entity] for entity in entity_set}
        return entity2id

    def __len__(self):
        return len(self.triples)

    def __getitem__(self, idx):
        head, relation, tail = self.triples[idx]
        return self.entity2id[head], self.relation2id[relation], self.entity2id[tail]

def load_data(filepath, load_all=False):
    entity_set = set()
    relation_set = set()
    triples = []

    if load_all:
        with open(filepath, 'r') as file:
            for line in file:
                head, relation, tail = line.strip().split('\t')
                entity_set.add(head)
                entity_set.add(tail)
                relation_set.add(relation)

        entity2id = {entity: idx for idx, entity in enumerate(entity_set)}
        relation2id = {relation: idx for idx, relation in enumerate(relation_set)}

        return entity2id, relation2id
    else:
        with open(filepath, 'r') as file:
            for line in file:
                head, relation, tail = line.strip().split('\t')
                triples.append((head, relation, tail))
        return triples

def build_adjacency_matrix(triples, entity2id):
    n_entities = max(entity2id.values()) + 1
    adj_matrix = np.zeros((n_entities, n_entities))

    for head, _, tail in triples:
        head_id = entity2id[head]
        tail_id = entity2id[tail]
        adj_matrix[head_id, tail_id] = 1

    adj_matrix = torch.tensor(adj_matrix, dtype=torch.float)
    return adj_matrix


if __name__ == '__main__':
    triples, entity2id, relation2id = load_data(os.path.join(os.path.dirname(__file__) ,r'data\WN18RR\train.txt'))
    adj_matrix = build_adjacency_matrix(triples, entity2id, relation2id)
    dataset = KnowledgeGraphDataset(triples, entity2id, relation2id)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    for data in dataloader:
        print(data)
