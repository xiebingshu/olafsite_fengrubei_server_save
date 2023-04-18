import torch
from torch.utils import data
from config import *
import pandas as pd
from Mission import NER_setting


# 加载词表
def get_vocab():
    df = pd.read_csv(NER_setting.VOCAB_PATH, names=['word', 'id'])
    return list(df['word']), dict(df.values) # id2word是list,word2id是dict


# 加载标签表
def get_label():
    df = pd.read_csv(NER_setting.LABEL_PATH, names=['label', 'id'])
    return list(df['label']), dict(df.values) # id2label是list,label2id是dict


# 解决句子不定长问题,dataloader无法整合成tensor的问题,找到batch里最长的数据，然后将其它填充成一样长
def collate_self(batch):
    batch.sort(key=lambda x: len(x[0]), reverse=True) # dataset get方法返回的是元组，所以x[0]才能拿到句子
    max_len = len(batch[0][0])
    input = []
    target = []
    mask = [] # crv模型的要求
    for item in batch:
        pad_num = max_len - len(item[0])
        input.append(item[0] + [NER_setting.WORD_PAD_ID] * pad_num)
        target.append(item[1] + [NER_setting.LABEL_O_ID] * pad_num)
        mask.append([1]*len(item[0]) + [0]*pad_num)
    return torch.tensor(input), torch.tensor(target), torch.tensor(mask).bool()


# 定义dataset
class Dataset(data.Dataset):
    def __init__(self, type='train', base_len=50):
        super().__init__()
        self.base_len = base_len
        if type == 'train':
            sample_path = NER_setting.TRAIN_SAMPLE_PATH
        else:
            sample_path = NER_setting.TEST_SAMPLE_PATH
        self.df = pd.read_csv(sample_path, names=['word', 'label'])
        self.word2id = get_vocab()[1] # dict
        self.label2id = get_label()[1] # dict
        self.points = self.get_points()

    def get_points(self):
        points = [0]
        index = 0
        while True:
            if self.df.loc[index + self.base_len, 'label'] == 'O':
                index += self.base_len
                points.append(index)
            else:
                index += 1
            if index + self.base_len >= len(self.df):
                points.append(len(self.df))
                break
        return points

    def __len__(self):
        return len(self.points)-1

    def __getitem__(self, index):
        df = self.df[self.points[index]:self.points[index+1]]
        unk_id = self.word2id[NER_setting.WORD_UNK]
        o_id = self.label2id['O']
        input = [self.word2id.get(word, unk_id) for word in df['word']]
        target = [self.label2id.get(label, o_id) for label in df['label']] # 保险机制,理论上没有其他标签（应该吧）
        return input, target


if __name__ == '__main__':
    dataset = Dataset()
    loader = data.DataLoader(dataset, batch_size=100, shuffle=True, collate_fn=collate_self)
