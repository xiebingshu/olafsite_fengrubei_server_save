import torch.nn as nn
from transformers import BertModel
import torch
import torch.nn.functional as f
from Mission import setting

from transformers import logging
logging.set_verbosity_error()


class CasRel(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = BertModel.from_pretrained(setting.BERT_MODEL_NAME)
        # 冻结Bert参数，训练的时候应该打开看下
        for name, param in self.bert.named_parameters():
            param.requires_grad = False
        self.sub_head_linear = nn.Linear(setting.BERT_DIM, 1)
        self.sub_tail_linear = nn.Linear(setting.BERT_DIM, 1)
        self.obj_head_linear = nn.Linear(setting.BERT_DIM, setting.REL_SIZE)
        self.obj_tail_linear = nn.Linear(setting.BERT_DIM, setting.REL_SIZE)

    def forward(self, input, mask):
        input_ids, sub_head_seq, sub_tail_seq = input
        encoded_text = self.get_encoded_text(input_ids, mask)
        # subject首尾序列预测
        pred_sub_head, pred_sub_tail = self.get_subs(encoded_text)

        # relation_object矩阵预测
        pred_obj_head, pred_obj_tail = self.get_objs_for_specific_sub(encoded_text, sub_head_seq, sub_tail_seq)

        return encoded_text, (pred_sub_head, pred_sub_tail, pred_obj_head, pred_obj_tail)

    # 利用bert将input_ids list 变成，length * bert_dim 矩阵
    def get_encoded_text(self, input_ids, mask):
        return self.bert(input_ids, attention_mask=mask)[0]

    def get_subs(self, encoded_text):
        # encode_text -> linear -> sigmoid激活
        pred_sub_head = torch.sigmoid(self.sub_head_linear(encoded_text))
        pred_sub_tail = torch.sigmoid(self.sub_tail_linear(encoded_text))
        return pred_sub_head, pred_sub_tail

    def get_objs_for_specific_sub(self, encoded_text, sub_head_seq, sub_tail_seq):
        # sub_head_seq.shape(batch_size, 句子长度)升维，(batch_size, 1 ,句子长度）
        sub_head_seq = sub_head_seq.unsqueeze(1).float()
        sub_tail_seq = sub_tail_seq.unsqueeze(1).float()

        # encoded_text.shape(batch_size, 句子长度， bert_dim), 相乘, 把1位的那个字拿出来
        sub_head = torch.matmul(sub_head_seq, encoded_text)
        sub_tail = torch.matmul(sub_tail_seq, encoded_text)
        encoded_text = encoded_text + (sub_head + sub_tail) / 2

        pred_obj_head = torch.sigmoid(self.obj_head_linear(encoded_text))
        pred_obj_tail = torch.sigmoid(self.obj_tail_linear(encoded_text))

        return pred_obj_head, pred_obj_tail
