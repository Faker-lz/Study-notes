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
    def __init__(self, graph_part_dir, entity2id, relation2id):
            self.graph_part_dir = graph_part_dir
            self.graph_part_files = [os.path.join(graph_part_dir, f) for f in os.listdir(graph_part_dir) if f.endswith('.txt')]
            self.entity2id = entity2id
            self.relation2id = relation2id

    def __len__(self):
        return len(self.graph_part_files)

    def __getitem__(self, idx):
        part_file = self.graph_part_files[idx]
        triples, _, _ = load_data(part_file, entity2id=self.entity2id, relation2id=self.relation2id)
        edge_index = build_edge_index(triples, self.entity2id)
        return edge_index, triples

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

def build_edge_index(triples, entity2id):
    """
    构建PyTorch Geometric格式的边索引
    :param triples: 知识图谱三元组列表，每个三元组是(head, relation, tail)
    :param entity2id: 实体到ID的映射字典
    :return: PyTorch Geometric格式的边索引
    """
    edges = []
    for head, relation, tail in triples:
        head_id = entity2id[head]
        tail_id = entity2id[tail]
        edges.append([head_id, tail_id])
    
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    return edge_index

if __name__ == '__main__':
    triples, entity2id, relation2id = load_data(os.path.join(os.path.dirname(__file__) ,r'data\WN18RR\train.txt'))
    adj_matrix = build_edge_index(triples, entity2id, relation2id)
    dataset = KnowledgeGraphDataset(triples, entity2id, relation2id)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    for data in dataloader:
        print(data)
