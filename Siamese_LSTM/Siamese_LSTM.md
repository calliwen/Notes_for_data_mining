
论文原文： [Siamese Recurrent Architectures for Learning Sentence Similarity](http://www.mit.edu/~jonasm/info/MuellerThyagarajan_AAAI16.pdf)

笔记参考：[](https://blog.csdn.net/sinat_31188625/article/details/72675627)

主要内容： 针对短语、句子、序列的相似性比较，提出一种评价模型--Siamese LSTM（孪生网络）。
模型输入是一对序列，输出为序列对的相似性得分。

模型框架结构如图：

[id]: model_framework.png  "Optional title attribute"


主要内容：利用LSTM 对不同长度的序列进行学习，将变长序列学习后得到固定维度的嵌入向量。 两个LSTM共享权重，具体实现方式为：反向传播进行参数更新时，取两个LSTM梯度的平均值进行更新。 最后对两个LSTM的结果计算 曼哈顿距离，利用exp()指数函数映射到[0, 1]之间，再对输出做相应的变换，将得分区间变换到了[1, 5]。

训练方式： 
损失函数： 预测得分与真实得分的均方差。
优化方法： AdaDelta.


几个可以参考的处理细节：
1. LSTM参数初始化，采用较小的高斯随机初始化遗忘门偏置参数值等。并利用其他相同问题的数据源进行预训练参数。

2. 数据增强；同义词辞典随即替换同义词，生成额外的训练sentence.


其他：
使用L1正则：

L2正则无法修正欧氏距离的梯度消失问题导致的对语义不同的句子误判为同类的error

本文的模型对于任何一种简单相似度方程具有很好的稳定性，但是Manhattan distance的效果略好于其他相似度方程（包括余弦相似度）






