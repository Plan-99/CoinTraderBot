import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

# 임의의 데이터셋 준비
np.random.seed(0)
data_size = 10000  # 데이터 크기
features = 2  # 주가와 거래량
seq_length = 50  # 시퀀스 길이

# 임의의 데이터 생성
data = np.random.rand(data_size, features).astype(np.float32)


# 시퀀스 데이터로 변환하는 함수
def create_sequences(data, seq_length):
    xs = []
    ys = []
    for i in range(len(data) - seq_length):
        x = data[i:(i + seq_length)]
        y = data[i + seq_length][0]  # 다음 시점의 주가 예측
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


x, y = create_sequences(data, seq_length)
x_tensor = torch.tensor(x).unsqueeze(1)  # CNN에 입력하기 위해 채널 차원 추가
y_tensor = torch.tensor(y)

# 데이터 로더 설정
batch_size = 100
dataset = TensorDataset(x_tensor, y_tensor)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)


# CNN 모델 정의
class CNNStockPredictor(nn.Module):
    def __init__(self):
        super(CNNStockPredictor, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=(5, 1), stride=(1, 1))
        self.conv2 = nn.Conv2d(16, 32, kernel_size=(5, 1), stride=(1, 1))
        self.fc1 = nn.Linear(32 * (seq_length - 8) * features, 128)
        self.fc2 = nn.Linear(128, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = x.view(x.size(0), -1)  # 플래튼
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# 모델, 손실 함수, 옵티마이저 초기화
model = CNNStockPredictor()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 학습 과정
num_epochs = 10

for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    for batch_idx, (data, target) in enumerate(dataloader):
        optimizer.zero_grad()
        print(np.shape(data))
        exit()
        output = model(data)
        loss = criterion(output.squeeze(), target)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    average_loss = total_loss / len(dataloader)
    print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {average_loss:.4f}')
