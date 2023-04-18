# 关系表的地址
REL_PATH = r"C:\Users\xiebingshu\BERT_CasRel_Data\output\rel.txt"
OBJ_SUB_PATH = r"C:\Users\xiebingshu\BERT_CasRel_Data\output\rel2entity.csv"
# 关系数量
REL_SIZE = 48
# 关系数据源
SCHEMA_DATA = r"C:\Users\xiebingshu\BERT_CasRel_Data\input\origin\DuIE2.0\duie_schema\duie_schema.json"
TRAIN_DATA = r"C:\Users\xiebingshu\BERT_CasRel_Data\input\origin\DuIE2.0\duie_train.json\duie_train.json"
TEST_DATA = r"C:\Users\xiebingshu\BERT_CasRel_Data\input\origin\DuIE2.0\duie_test2.json\duie_test2.json"
DEV_DATA = r"C:\Users\xiebingshu\BERT_CasRel_Data\input\origin\DuIE2.0\duie_dev.json\duie_dev.json"

BERT_MODEL_NAME = 'bert-base-chinese'
import torch

DEVICE = torch.device("cuda")

BATCH_SIZE = 100
BERT_DIM = 768
LEARING_RATE = 5e-5
EPOCH = 50
MODEL_DIR = r"C:\Users\xiebingshu\BERT_CasRel_Data\output\model"

CLS_WEIGHT_COEF = [0.3, 1.0] #权重矩阵
SUB_WEIGHT_COEF = 3

SUB_HEAD_BAR = 0.5
SUB_TAIL_BAR = 0.5
OBJ_HEAD_BAR = 0.5
OBJ_TAIL_BAR = 0.5

EPS = 1e-10