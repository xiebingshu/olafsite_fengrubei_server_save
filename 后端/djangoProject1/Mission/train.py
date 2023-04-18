import torch.nn as nn
from TorchCRF import CRF
import torch
from Mission import setting
from Mission import utils
from torch.utils import data
import tqdm
from Mission import model
import torch.nn.functional as f


def calc_loss(pred, true, mask):
    true = true.float()
    # 降维
    pred = pred.squeeze(-1)
    weight = torch.where(true > 0, setting.CLS_WEIGHT_COEF[1], setting.CLS_WEIGHT_COEF[0])
    loss = f.binary_cross_entropy(pred, true, weight=weight, reduction='none')
    if loss.shape != mask.shape:
        mask = mask.unsqueeze(-1)
    return torch.sum(loss * mask) / torch.sum(mask)


def loss_fn(true_y, pred_y, mask):
    pred_sub_head, pred_sub_tail, pred_obj_head, pred_obj_tail = pred_y
    true_sub_head, true_sub_tail, true_obj_head, true_obj_tail = true_y
    # print('sub_head:', calc_loss(pred_sub_head, true_sub_head, mask).item(), 'sub_tail', calc_loss(pred_sub_tail, true_sub_tail, mask).item(), 'obj_head:', calc_loss(pred_obj_head, true_obj_head, mask).item(), 'obj_tail', calc_loss(pred_obj_tail, true_obj_tail, mask).item())
    return calc_loss(pred_sub_head, true_sub_head, mask) * setting.SUB_WEIGHT_COEF + calc_loss(pred_sub_tail, true_sub_tail, mask) * setting.SUB_WEIGHT_COEF+ calc_loss(pred_obj_head, true_obj_head, mask) + calc_loss(pred_obj_tail, true_obj_tail, mask)


def report(model, encoded_text, pred_y, batch_text, batch_mask):
    pred_sub_head, pred_sub_tail, _, _ = pred_y
    true_triple_list = batch_text['triple_list']
    pred_triple_list = []

    correct_num, predict_num, gold_num = 0, 0, 0

    for i in range(len(pred_sub_head)):
        text = batch_text['text'][i]
        true_triple_item = true_triple_list[i]
        mask = batch_mask[i]
        offset_mapping = batch_text['offset_mapping'][i]
        sub_head_ids = torch.where(pred_sub_head[i] > setting.SUB_HEAD_BAR)[0]
        sub_tail_ids = torch.where(pred_sub_tail[i] > setting.SUB_TAIL_BAR)[0]

        pred_triple_item = get_triple_list(sub_head_ids, sub_tail_ids, model, encoded_text[i], text, mask, offset_mapping)
        correct_num += len(set(true_triple_item) & set(pred_triple_item))
        predict_num += len(set(pred_triple_item))
        gold_num += len(set(true_triple_item))

        pred_triple_list.append(pred_triple_item)

    precision = correct_num / (predict_num + setting.EPS)
    recall = correct_num / (gold_num + setting.EPS)
    f1_score = 2 * precision * recall / (precision + recall + setting.EPS)
    print('\tcorrect_num:', correct_num, 'predict_num:', predict_num, 'gold_num:', gold_num)
    print('\tprecision:%.3f' % precision, 'recall:%.3f' % recall, 'f1_score:%.3f' % f1_score)


def get_triple_list(sub_head_ids, sub_tail_ids, model, encoded_text, text, mask, offset_mapping):
    id2rel, _ = utils.get_rel()
    triple_list = []
    for sub_head_id in sub_head_ids:
        sub_tail_ids = sub_tail_ids[sub_tail_ids >= sub_head_id]
        if len(sub_tail_ids) == 0:
            continue
        sub_tail_id = sub_tail_ids[0]
        if mask[sub_head_id] == 0 or mask[sub_tail_id] == 0:
            continue
        sub_head_pos_id = offset_mapping[sub_head_id][0]
        sub_tail_pos_id = offset_mapping[sub_tail_id][1]
        subject_text = text[sub_head_pos_id:sub_tail_pos_id]
        sub_head_seq = torch.tensor(utils.multihot(len(mask), sub_head_id)).to(setting.DEVICE)
        sub_tail_seq = torch.tensor(utils.multihot(len(mask), sub_tail_id)).to(setting.DEVICE)
        pred_obj_head, pred_obj_tail = model.get_objs_for_specific_sub(encoded_text.unsqueeze(0), sub_head_seq.unsqueeze(0), sub_tail_seq.unsqueeze(0))
        pred_obj_head = pred_obj_head[0].T
        pred_obj_tail = pred_obj_tail[0].T
        for j in range(len(pred_obj_head)):
            obj_head_ids = torch.where(pred_obj_head[j] > setting.OBJ_HEAD_BAR)[0]
            obj_tail_ids = torch.where(pred_obj_tail[j] > setting.OBJ_TAIL_BAR)[0]
            for obj_head_id in obj_head_ids:
                obj_tail_ids = obj_tail_ids[obj_tail_ids >= obj_head_id]
                if len(obj_tail_ids) == 0:
                    continue
                obj_tail_id = obj_tail_ids[0]
                if mask[obj_head_id] == 0 or mask[obj_tail_id] == 0:
                    continue

                obj_head_pos_id = offset_mapping[obj_head_id][0]
                obj_tail_pos_id = offset_mapping[obj_tail_id][1]
                object_text = text[obj_head_pos_id:obj_tail_pos_id]
                triple_list.append((subject_text, id2rel[j], object_text))
    return list(set(triple_list))


if __name__ == '__main__':
    model = model.CasRel().to(setting.DEVICE)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=setting.LEARING_RATE)
    
    dataset = utils.Dataset()
    for i in range(setting.EPOCH):
        loader = data.DataLoader(dataset, batch_size=setting.BATCH_SIZE, shuffle=True, collate_fn=utils.collate_myself)
        for b, (batch_mask, batch_x, batch_y) in enumerate(loader):
            batch_text, batch_sub_rnd = batch_x
            batch_sub, batch_obj_rel = batch_y

            # 拿到dataloader里的数据，进行处理
            input_mask = torch.tensor(batch_mask).to(setting.DEVICE)
            input = (
                torch.tensor(batch_text['input_ids']).to(setting.DEVICE),
                torch.tensor(batch_sub_rnd['head_seq']).to(setting.DEVICE),
                torch.tensor(batch_sub_rnd['tail_seq']).to(setting.DEVICE)
            )
            # return encoded_text, (pred_sub_head, pred_sub_tail, pred_obj_head, pred_obj_tail)
            encoded_text, pred_y = model(input, input_mask) # 拿到预测值
            # 整理target数据
            true_y = (
                torch.tensor(batch_sub['heads_seq']).to(setting.DEVICE),
                torch.tensor(batch_sub['tails_seq']).to(setting.DEVICE),
                torch.tensor(batch_obj_rel['heads_mx']).to(setting.DEVICE),
                torch.tensor(batch_obj_rel['tails_mx']).to(setting.DEVICE)
            )

            loss = loss_fn(true_y, pred_y, input_mask)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if b % 50 == 0:
                print('>>epoch:', i, 'batch:', b, 'loss', loss.item())
            if b % 500 == 0 and b != 0:
                report(model, encoded_text, pred_y, batch_text, batch_mask)
        if i % 3 == 0:
            torch.save(model, setting.MODEL_DIR + f'model_{i}.pth')