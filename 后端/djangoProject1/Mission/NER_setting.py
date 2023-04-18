import torch

ORIGIN_LOC = r"C:\Users\xiebingshu\NER_DATA\input\origin\people_dairy_2014.json"
PROCESS_DIR = r"C:\Users\xiebingshu\NER_DATA\input\process"

TRAIN_SAMPLE_PATH = r"C:\Users\xiebingshu\NER_DATA\output\train_sample.txt"
TEST_SAMPLE_PATH = r"C:\Users\xiebingshu\NER_DATA\output\test_sample.txt"

VOCAB_PATH = r"C:\Users\xiebingshu\NER_DATA\output\vocab.txt"  # 词表
LABEL_PATH = r"C:\Users\xiebingshu\NER_DATA\output\label.txt"  # 标签表，虽然是最基础的（叹气）

WORD_PAD = '<PAD>' # 空置词，词表0
WORD_UNK = 'UNK' # 未知词，词表1

WORD_PAD_ID = 0
WORD_UNK_ID = 1
LABEL_O_ID = 0

VOCAB_SIZE = 3000 # 中文常用词大概3000
EMBEDDING_DIM = 100
HIDDEN_SIZE = 256
TARGET_SIZE = 9
LEARING_RATE = 1e-3
EPOCH = 100

MODEL_DIR = r"C:\Users\xiebingshu\NER_DATA\output\model"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

per_replace_words = ['他', '她', '你', '您']
loc_replace_words = ['这儿', '这里', '那儿', '那里']
org_replace_words = ['他们', '她们']