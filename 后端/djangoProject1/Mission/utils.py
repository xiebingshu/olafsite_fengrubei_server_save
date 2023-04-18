import torch.utils.data as data
import pandas as pd
import random
import json
from transformers import BertTokenizerFast
from Mission import setting


def get_rel():
    df = pd.read_csv(setting.REL_PATH, names=['rel', 'id'])
    return df['rel'].tolist(), dict(df.values) #get_rel[0] id2rel,是list get_rel[1] rel2id 是dict


def multihot(length, hot_pos):
    return [1 if i in hot_pos else 0 for i in range(length)]


def collate_myself(batch):
    batch.sort(key=lambda x: len(x['input_ids']), reverse=True)
    max_len = len(batch[0]['input_ids'])
    batch_text = {
        'text': [],
        'input_ids': [],
        'offset_mapping': [],
        'triple_list': []
    }
    batch_mask = []
    batch_sub = {
        'heads_seq': [],
        'tails_seq': []
    }
    batch_sub_rnd = {
        'head_seq': [],
        'tail_seq': []
    }
    batch_obj_rel = {
        'heads_mx': [],
        'tails_mx': []
    }
    for item in batch:
        # 将不同的句子补充成相同的长度，组织tensor
        input_ids = item['input_ids']
        item_len = len(input_ids)
        pad_num = max_len - item_len
        input_ids = input_ids + [0] * pad_num
        mask = [1] * item_len + [0] * pad_num
        # 填充subject的one-hot列表
        sub_heads_seq = multihot(max_len, item['sub_head_ids'])
        sub_tails_seq = multihot(max_len, item['sub_tail_ids'])
        # 随机选择一个sub，用于预测
        if len(item['triple_id_list']) == 0: # 理论上不会有这种情况发生
            continue
        sub_rnd = random.choice(item['triple_id_list'])[0]
        sub_rnd_head_seq = multihot(max_len, [sub_rnd[0]])
        sub_rnd_tail_seq = multihot(max_len, [sub_rnd[1]])
        # 根据随机subject来生成relations矩阵，size = 字数 * 种类数
        obj_head_mx = [[0] * setting.REL_SIZE for i in range(max_len)]
        obj_tail_mx = [[0] * setting.REL_SIZE for i in range(max_len)]
        for triple in item['triple_id_list']:
            rel_id = triple[1]
            head_id, tail_id = triple[2]
            if triple[0] == sub_rnd:
                obj_head_mx[head_id][rel_id] = 1
                obj_tail_mx[tail_id][rel_id] = 1
        # 将数据组装成batch的格式
        batch_text['text'].append(item['text'])
        batch_text['input_ids'].append(input_ids)
        batch_text['offset_mapping'].append(item['offset_mapping'])
        batch_text['triple_list'].append(item['triple_list'])
        batch_mask.append(mask)
        batch_sub['heads_seq'].append(sub_heads_seq)
        batch_sub['tails_seq'].append(sub_tails_seq)
        batch_sub_rnd['head_seq'].append(sub_rnd_head_seq)
        batch_sub_rnd['tail_seq'].append(sub_rnd_tail_seq)
        batch_obj_rel['heads_mx'].append(obj_head_mx)
        batch_obj_rel['tails_mx'].append(obj_tail_mx)
    return batch_mask, (batch_text, batch_sub_rnd), (batch_sub, batch_obj_rel)


class Dataset(data.Dataset):
    def __init__(self, type='train'):
        super().__init__()
        self.rel2id = get_rel()[1]
        # 解析文件路径，做测试的准备
        if type == 'train':
            file_path = setting.TRAIN_DATA
        elif type == 'test':
            file_path = setting.TEST_DATA
        else:
            file_path = setting.DEV_DATA
        with open(file_path, encoding='utf-8') as f:
            self.lines = f.readlines()
        self.tokenizer = BertTokenizerFast.from_pretrained(setting.BERT_MODEL_NAME)

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        line = self.lines[index]
        info = json.loads(line)
        tokenized = self.tokenizer(info['text'], return_offsets_mapping=True)
        info['input_ids'] = tokenized['input_ids']
        info['offset_mapping'] = tokenized['offset_mapping']

        return self.parse_json(info)

    def parse_json(self, info):
        text = info['text']
        input_ids = info['input_ids']
        dct = {
            'text': text,
            'input_ids': input_ids,
            'offset_mapping': info['offset_mapping'],
            'sub_head_ids': [],
            'sub_tail_ids': [],
            'triple_list': [],
            'triple_id_list': []
        }
        for spo in info['spo_list']:
            subject = spo['subject']
            object = spo['object']['@value']
            predicate = spo['predicate']
            dct['triple_list'].append((subject, predicate, object))
            # 获得sub_head_id, sub_tail_id
            subject_tmp = self.tokenizer(subject, add_special_tokens=False)
            sub_token = subject_tmp['input_ids']
            sub_pos_id = self.get_pos_id(input_ids, sub_token)
            if not sub_pos_id:
                continue
            sub_head_id, sub_tail_id = sub_pos_id
            # 获得object_head_id, object_tail-id
            object_tmp = self.tokenizer(object, add_special_tokens=False)
            obj_token = object_tmp['input_ids']
            obj_pos_id = self.get_pos_id(input_ids, obj_token)
            if not obj_pos_id:
                continue
            obj_head_id, obj_tail_id = obj_pos_id
            # 完善dict
            dct['sub_head_ids'].append(sub_head_id)
            dct['sub_tail_ids'].append(sub_tail_id)
            dct['triple_id_list'].append(([sub_head_id, sub_tail_id], self.rel2id[predicate], [obj_head_id, obj_tail_id]))
        return dct

    def get_pos_id(self, source, elem):
        for head_id in range(len(source)):
            tail_id = head_id + len(elem)
            if source[head_id:tail_id] == elem:
                return head_id, tail_id-1


if __name__ == '__main__':
    dataset = Dataset()
    loader = data.DataLoader(dataset, batch_size=2, shuffle=False, collate_fn=collate_myself)
    print(iter(loader).__next__())
