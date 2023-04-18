from Mission.NER_setting import *
from Mission.NER_utils import *
import jieba
import re
from Mission.NER_model import Model


class Obj_item:
    def __init__(self, name, type):
        self.name = name
        self.type = type


def sentence_NER(sentence, obj_dict):
    text = sentence
    word2id = get_vocab()[1]
    input = torch.tensor([[word2id.get(w, WORD_UNK_ID) for w in text]]).to(device)
    mask = torch.tensor([[1] * len(text)]).bool().to(device)

    model = torch.load(r'E:\谢秉书\Desktop\知识图谱\djangoProject\index\model\modelmodel_4.pth')

    y_pred = model(input, mask)
    id2label = get_label()[0]

    label = [id2label[l] for l in y_pred[0]]
    head_tmp = -1
    tail_tmp = -1
    type_save = ''
    for pos, l in enumerate(label):
        if re.match('B-', l) != None:
            head_tmp = pos
            type_tmp = l[2:]
            type_save = l[2:]
            if type_tmp == 'PER':
                type_tmp = '人物'
            elif type_tmp == 'LOC':
                type_tmp = '地点'
            elif type_tmp == 'T':
                type_tmp = '时间'
            elif type_tmp == 'ORG':
                type_tmp = '组织'
        if re.match('I-', l) != None and head_tmp != -1 and l[2:] == type_save:
            tail_tmp = pos
        elif re.match('I-', l) != None and head_tmp != -1 and l[2:] != type_save:
            add_or_not = True
            for item in obj_dict:
                if item.name == text[head_tmp:tail_tmp + 1]:
                    add_or_not = False
                    break
            if add_or_not:
                obj_dict.append(Obj_item(text[head_tmp:tail_tmp + 1], type_tmp))
            tail_tmp = -1
            head_tmp = pos
            type_tmp = l[2:]
            type_save = l[2:]
            if type_tmp == 'PER':
                type_tmp = '人物'
            elif type_tmp == 'LOC':
                type_tmp = '地点'
            elif type_tmp == 'T':
                type_tmp = '时间'
            elif type_tmp == 'ORG':
                type_tmp = '组织'
        elif l == 'O' and head_tmp != -1 and tail_tmp != -1:
            add_or_not = True
            for item in obj_dict:
                if item.name == text[head_tmp:tail_tmp + 1]:
                    add_or_not = False
                    break
            if add_or_not:
                obj_dict.append(Obj_item(text[head_tmp:tail_tmp + 1], type_tmp))
            head_tmp = -1
            tail_tmp = -1
        elif l == 'O' and head_tmp != -1 and tail_tmp == -1:
            head_tmp = -1


def bert_replace(sentence, obj_dict):
    words = jieba.lcut(sentence)
    # print(words)
    for i, word in enumerate(words):
        if word in per_replace_words:
            for obj in obj_dict[::-1]:
                if obj.type == 'PER':
                    words[i] = obj.name
                    # print(word, obj.name)
                    break
        if word in loc_replace_words:
            for obj in obj_dict[::-1]:
                if obj.type == 'LOC':
                    words[i] = obj.name
                    # print(word, obj.name)
                    break
        if word in org_replace_words:
            for obj in obj_dict[::-1]:
                if obj.type == 'ORG':
                    words[i] = obj.name
                    # print(word, obj.name)
                    break
    print(''.join(words))
    return ''.join(words)



