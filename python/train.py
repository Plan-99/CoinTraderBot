import torch
import torch.nn as nn
import numpy as np
import math
import pymysql
from dotenv import load_dotenv
import os
import pandas as pd
from torch.utils.data import DataLoader, Dataset
from constants import WINDOW_LEN, TARGET_GAP, NUM_LAYERS, HIDDEN_DIM, BATCH_SIZE, \
    LEARNING_RATE, EPOCHS

load_dotenv()
conn = pymysql.connect(host=os.getenv('DB_HOST'),
                       user=os.getenv('DB_USER'),
                       password=os.getenv('DB_PASSWORD'),
                       db=os.getenv('DB_NAME'),
                       charset='utf8')
cursor = conn.cursor()

query = "SELECT COUNT(idx) FROM candles GROUP BY symbol ORDER BY COUNT(idx)"
cursor.execute(query)
least = cursor.fetchone()[0]

query = "SELECT AVG(trade_price), STD(trade_price) FROM candles"
cursor.execute(query)
res = cursor.fetchone()
trade_price_avg, trade_price_std = res[0], res[1]

query = "SELECT symbol, opening_price, trade_price FROM candles ORDER BY symbol, timestamp"
cursor.execute(query)
_data = cursor.fetchall()


def fetch_data_from_db(data, window_len, target_gap, trade_price_avg, trade_price_std):
    group_list = []
    item_group = []
    symbol = data[0][0]
    for i in range(len(data) - 1):
        item = data[i]

        next_item = data[i + 1]
        diff = ((next_item[1] - item[1]) / item[1]) * 100
        normalized_trade_price = (item[2] - trade_price_avg) / trade_price_std
        if next_item[0] == symbol:
            if len(item_group) < least - 1:
                item_group.append([diff, normalized_trade_price])
        else:
            group_list.append(item_group)
            item_group = []
            symbol = next_item[0]

    train_dataset_list = []
    test_dataset_list = []
    train_target_list = []
    test_target_list = []
    for group in group_list:
        for i in range(len(group) - window_len - target_gap):
            train_data_len = (len(group) - window_len - target_gap) * 0.8
            seq_data = group[i:i + window_len]
            target = 0
            for j in range(target_gap):
                target += group[i + window_len + j + 1][0]

            if i < train_data_len:
                train_dataset_list.append(seq_data)
                train_target_list.append(target)
            else:
                test_dataset_list.append(seq_data)
                test_target_list.append(target)

    return train_dataset_list, train_target_list, test_dataset_list, test_target_list


fetched_data_train, target_train, fetched_data_test, target_test = fetch_data_from_db(_data, WINDOW_LEN, TARGET_GAP, trade_price_avg, trade_price_std)


class StockDataset(Dataset):
    def __init__(self, dataset_list, target_list):
        self.data = torch.tensor(dataset_list, dtype=torch.float32).unsqueeze(1)
        self.targets = torch.tensor(target_list, dtype=torch.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]


train_dataset = StockDataset(fetched_data_train, target_train)
test_dataset = StockDataset(fetched_data_test, target_test)

train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=True)


class CNNModel(nn.Module):
    def __init__(self, seq_length, features):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=(5, 1), stride=(1, 1))
        self.conv2 = nn.Conv2d(16, 32, kernel_size=(5, 1), stride=(1, 1))
        self.fc1 = nn.Linear(32 * (seq_length - 8) * features, 128)
        self.fc2 = nn.Linear(128, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.relu(self.conv2(x))
        x = x.view(x.size(0), -1)  # 플래튼
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# 모델 초기화
model = CNNModel(WINDOW_LEN, 2)

# 손실 함수 및 최적화 알고리즘 설정
criterion = nn.MSELoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)


model.train()
for epoch in range(EPOCHS):
    total_loss = 0
    for batch, targets in train_dataloader:
        optimizer.zero_grad()
        outputs = model(batch)
        loss = criterion(outputs, targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5)
        optimizer.step()
        total_loss += loss.item()

    average_loss = total_loss / len(train_dataloader)
    print(f'Epoch {epoch + 1}, Loss: {loss.item()}')
