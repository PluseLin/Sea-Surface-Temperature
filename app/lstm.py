import pandas as pd
import numpy as np
import torch
from torch import nn, optim
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from utils import *

# 假设我们有一个数据框，其中包括时间、经度、纬度和温度
# 数据框格式例如：
# data = pd.DataFrame({
#     'time': [...],
#     'longitude': [...],
#     'latitude': [...],
#     'temperature': [...]
# })

data = nc.Dataset("../data/ERRST/ersst.201401.nc", 'r')

# 对时间进行处理，转换为序列数据
data['time'] = pd.to_datetime(data['time'])
data['time'] = data['time'].map(pd.Timestamp.timestamp)

# 选择特征和目标变量
features = data[['time', 'longitude', 'latitude']].values
target = data['temperature'].values

# 数据标准化
scaler = MinMaxScaler()
features = scaler.fit_transform(features)
target = scaler.fit_transform(target.reshape(-1, 1))

# 将数据划分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# 将数据转换为 PyTorch 张量
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

class LSTMPredictor(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMPredictor, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

input_size = 3  # time, longitude, latitude
hidden_size = 50
num_layers = 2
output_size = 1  # temperature

model = LSTMPredictor(input_size, hidden_size, num_layers, output_size)

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 100
batch_size = 64

# 创建数据加载器
train_loader = torch.utils.data.DataLoader(dataset=list(zip(X_train, y_train)), batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=list(zip(X_test, y_test)), batch_size=batch_size, shuffle=False)

for epoch in range(num_epochs):
    model.train()
    for i, (x_batch, y_batch) in enumerate(train_loader):
        outputs = model(x_batch.unsqueeze(1))
        loss = criterion(outputs, y_batch)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

model.eval()
with torch.no_grad():
    predictions = []
    actuals = []
    for x_batch, y_batch in test_loader:
        outputs = model(x_batch.unsqueeze(1))
        predictions.append(outputs)
        actuals.append(y_batch)
    
    predictions = torch.cat(predictions).cpu().numpy()
    actuals = torch.cat(actuals).cpu().numpy()

# 反归一化
predictions = scaler.inverse_transform(predictions)
actuals = scaler.inverse_transform(actuals)

# 计算误差
mse = np.mean((predictions - actuals) ** 2)
print(f'Mean Squared Error on test set: {mse:.4f}')
