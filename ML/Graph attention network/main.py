from train import KnowledgeGraphTrainer


def main():
    trainer = KnowledgeGraphTrainer(
        r'E:\study\now\研究生\学习笔记\ML\Graph attention network\data\WN18RR\all.txt',
        r'E:\study\now\研究生\学习笔记\ML\Graph attention network\data\WN18RR\train.txt',
        r'E:\study\now\研究生\学习笔记\ML\Graph attention network\data\WN18RR\valid.txt',
        3,
        768,
        768,
        0.2,
        0.2,
        3,
        128,
        0.005,
        50
    )
    print('start trainning ...')
    trainer.train_epoch()

if __name__ == '__main__':
    main()