import torch.nn as nn
from config import *
from TorchCRF import CRF
import torch
from Mission.NER_setting import *
from Mission.NER_utils import *
from torch.utils import data
import tqdm


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM, WORD_PAD_ID)
        self.lstm = nn.LSTM(
            EMBEDDING_DIM,
            HIDDEN_SIZE,
            batch_first=True,
            bidirectional=True,
        )
        self.linear = nn.Linear(2 * HIDDEN_SIZE, TARGET_SIZE)
        self.crf = CRF(num_labels=TARGET_SIZE)

    def _get_lstm_feature(self, input):
        out = self.embed(input)
        out = self.lstm(out)[0]
        return self.linear(out)

    def forward(self, input, mask):
        out = self._get_lstm_feature(input)
        return self.crf.viterbi_decode(out, mask)

    def loss_fn(self, input, target, mask):
        y_pred = self._get_lstm_feature(input)
        return -self.crf.forward(y_pred, target, mask).mean().to(device)


if __name__ == '__main__':
    dataset = Dataset()
    loader = data.DataLoader(
        dataset,
        batch_size=100,
        shuffle=True,
        collate_fn=collate_self,
    )

    model = Model().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARING_RATE)

    for epoch in range(EPOCH):
        for i, (input, target, mask) in tqdm.tqdm(enumerate(loader)):
            input = input.to(device)
            target = target.to(device)
            mask = mask.to(device)
            y_pred = model(input, mask)
            loss = model.loss_fn(input, target, mask)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if i % 10 == 0:
                print(">> epoch:", epoch, "loss", loss.item(), " ", i/len(dataset))
        torch.save(model, MODEL_DIR + f'model_{epoch}.pth')


