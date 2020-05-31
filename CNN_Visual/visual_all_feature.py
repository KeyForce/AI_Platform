# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.conv1(x)
        draw_features(2, 3, x.cpu().detach().numpy(), "{}/f1_conv1.png".format('./heatmat'))

        x = F.relu(x)
        draw_features(2, 3, x.cpu().detach().numpy(), "{}/f1_relu1.png".format('./heatmat'))

        x = self.pool1(x)
        draw_features(2, 3, x.cpu().detach().numpy(), "{}/f1_pool1.png".format('./heatmat'))

        x = self.conv2(x)
        draw_features(4, 4, x.cpu().detach().numpy(), "{}/f1_conv2.png".format('./heatmat'))

        x = F.relu(x)
        draw_features(4, 4, x.cpu().detach().numpy(), "{}/f1_relu2.png".format('./heatmat'))

        x = self.pool2(x)
        draw_features(4, 4, x.cpu().detach().numpy(), "{}/f1_pool2.png".format('./heatmat'))

        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    # 定义权值初始化
    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                torch.nn.init.xavier_normal_(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                torch.nn.init.normal_(m.weight.data, 0, 0.01)
                m.bias.data.zero_()


def draw_features(width, height, x, savename):
    """
    画出heatmap，width*heigh = channel
    :param width: matplot的列
    :param height: matplot的行
    :param x: 经过运算的数据
    :param savename: 保存位置
    :return: 无
    """
    tic = time.time()
    fig = plt.figure(figsize=(16, 16))
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.05, hspace=0.05)
    for i in range(width * height):
        plt.subplot(height, width, i + 1)
        plt.axis('off')
        img = x[0, i, :, :]
        pmin = np.min(img)
        pmax = np.max(img)
        img = ((img - pmin) / (pmax - pmin + 0.000001)) * 255
        img = img.astype(np.uint8)
        img = cv2.applyColorMap(img, cv2.COLORMAP_JET)
        img = img[:, :, ::-1]  # 注意cv2（BGR）和matplotlib(RGB)通道是相反的
        plt.imshow(img)
        # plt.show()
        print("{}/{}".format(i, width * height))
    fig.savefig(savename, dpi=100)
    fig.clf()
    plt.close()
    print("time:{}".format(time.time() - tic))


pretrained_path = './net_params_72p.pkl'

# 建立模型
model = Net().cuda()
pretrained_dict = torch.load(pretrained_path)
model.load_state_dict(pretrained_dict)

# 数据预处理
Transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize([0.49139968, 0.48215827, 0.44653124],
                         [0.24703233, 0.24348505, 0.26158768])
])
img = cv2.imread('./cat.png')
img = Image.fromarray(img)
img = Transform(img).cuda()
img = img.unsqueeze(0)

start = time.time()
out = model(img)
end = time.time()
