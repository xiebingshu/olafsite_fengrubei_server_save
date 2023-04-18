from transformers import BertTokenizerFast
from Mission.setting import *
from Mission.model import *
from Mission.utils import *
from Mission.train import *


class Rel_item:
    def __init__(self, sub, type, obj):
        self.sub = sub
        self.type = type
        self.obj = obj


class Obj_item:
    def __init__(self, name, type):
        self.name = name
        self.type = type


def get_entity():
    df = pd.read_csv(OBJ_SUB_PATH, names=['sub', 'obj', 'id'])
    return df['sub'].tolist(), df['obj'].tolist() #0 id2sub, 1 id2obj


def sentence_Casrel(sentence, obj_dict, rel_dict):
    text = sentence
    print(text)
    aid_index = False
    if len(text) >= 30 and '，' in text:
        sentences_split = text.split('，')
        aid_index = 1
    sentences_aid = []
    tokenizer = BertTokenizerFast.from_pretrained(BERT_MODEL_NAME)
    tokenized = tokenizer(text, return_offsets_mapping=True)
    info = {}
    info['input_ids'] = tokenized['input_ids']
    info['offset_mapping'] = tokenized['offset_mapping']
    info['mask'] = tokenized['attention_mask']

    input_ids = torch.tensor([info['input_ids']]).to(DEVICE)
    batch_mask = torch.tensor([info['mask']]).to(DEVICE)

    model = torch.load(r'E:\谢秉书\Desktop\知识图谱\djangoProject\index\model\model_18.pth')
    encoded_text = model.get_encoded_text(input_ids, batch_mask)
    pred_sub_head, pred_sub_tail = model.get_subs(encoded_text)

    sub_head_ids = torch.where(pred_sub_head[0] > SUB_HEAD_BAR)[0]
    sub_tail_ids = torch.where(pred_sub_tail[0] > SUB_TAIL_BAR)[0]

    mask = batch_mask[0]
    encoded_text = encoded_text[0]

    offset_mapping = info['offset_mapping']
    pred_triple_item = get_triple_list(sub_head_ids, sub_tail_ids, model, encoded_text, text, mask, offset_mapping)
    for item in list(set([i[0] for i in pred_triple_item])):
        if aid_index == 1:
            for sen in sentences_split:
                sentences_aid.append(item + sen)
            for sen in sentences_split:
                sentences_aid.append(sen)
    for item in pred_triple_item:
        add_or_not0 = True
        for rel_exist in rel_dict:
            if rel_exist.sub == item[0] and rel_exist.type == item[1] and rel_exist.obj == item[2]:
                add_or_not0 = False
                break
        if add_or_not0:
            rel_dict.append(Rel_item(item[0], item[1], item[2]))
        add_or_not1 = True
        add_or_not2 = True
        for i in obj_dict:
            if item[0] == i.name:
                add_or_not1 = False
            if item[2] == i.name:
                add_or_not2 = False
            if add_or_not1 == False and add_or_not2 == False:
                break
        if add_or_not1:
            obj_dict.append(Obj_item(item[0], get_entity()[0][get_rel()[1].get(item[1])]))
        if add_or_not2:
            obj_dict.append(Obj_item(item[2], get_entity()[1][get_rel()[1].get(item[1])]))
    print(pred_triple_item)
    if aid_index == 1:
        for sen in sentences_aid:
            sentence_Casrel_aid(sen, obj_dict, rel_dict)


def sentence_Casrel_aid(sentence, obj_dict, rel_dict):
    print("aid_begin: ",sentence)
    text = sentence
    tokenizer = BertTokenizerFast.from_pretrained(BERT_MODEL_NAME)
    tokenized = tokenizer(text, return_offsets_mapping=True)
    info = {}
    info['input_ids'] = tokenized['input_ids']
    info['offset_mapping'] = tokenized['offset_mapping']
    info['mask'] = tokenized['attention_mask']

    input_ids = torch.tensor([info['input_ids']]).to(DEVICE)
    batch_mask = torch.tensor([info['mask']]).to(DEVICE)

    model = torch.load(r'E:\谢秉书\Desktop\知识图谱\djangoProject\index\model\model_18.pth')
    encoded_text = model.get_encoded_text(input_ids, batch_mask)
    pred_sub_head, pred_sub_tail = model.get_subs(encoded_text)

    sub_head_ids = torch.where(pred_sub_head[0] > SUB_HEAD_BAR)[0]
    sub_tail_ids = torch.where(pred_sub_tail[0] > SUB_TAIL_BAR)[0]

    mask = batch_mask[0]
    encoded_text = encoded_text[0]

    offset_mapping = info['offset_mapping']

    pred_triple_item = get_triple_list(sub_head_ids, sub_tail_ids, model, encoded_text, text, mask, offset_mapping)
    for item in pred_triple_item:
        add_or_not0 = True
        for rel_exist in rel_dict:
            if rel_exist.sub == item[0] and rel_exist.type == item[1] and rel_exist.obj == item[2]:
                add_or_not0 = False
                break
        if add_or_not0:
            rel_dict.append(Rel_item(item[0], item[1], item[2]))
        add_or_not1 = True
        add_or_not2 = True
        for i in obj_dict:
            if item[0] == i.name:
                add_or_not1 = False
            if item[2] == i.name:
                add_or_not2 = False
            if add_or_not1 == False and add_or_not2 == False:
                break
        if add_or_not1:
            obj_dict.append(Obj_item(item[0], get_entity()[0][get_rel()[1].get(item[1])]))
        if add_or_not2:
            obj_dict.append(Obj_item(item[2], get_entity()[1][get_rel()[1].get(item[1])]))
    print(pred_triple_item)