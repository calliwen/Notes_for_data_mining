# Modelling Sentence Pairs with Tree-structured Attentive Encoder

## 主要内容

提出了一种 attentive encoder that combines tree-structured RNN and Sequential RNN for modeling sentences pairs.

结合 tree-structured RNN 和 Sequential RNN 两种的 注意力 Encoder.

## 实验数据集

semantic similarity on SICK;
paraphrase identification on MSRP;
true-false question selection on AI2-8grade science questions;

## 模型架构

模型的整体框架如下：
![Model Structured][Model_Structure]

其中，最主要的部分是，Att Tree-RNNs 结构，这是将句子 encoder 成句子表征的核心部分。 本文提出了两种 attention Tree-RNNs; 分别是 att Tree-LSTM 和 att Tree-GRU.

这两种结构详细结构图如下：
![Tree RNNs Structure][Tree_RNNs_Structure]

分别对 LSTM 和 GRU 应用 Child-Sum algorithm.

## Standard Tree-RNNs

### Child-Sum Tree-LSTM

Child-Sum Tree-LSTM  包含两个部分： external part 和 internal part.
1. External part.

inputs 和 outputs. 

the inputs of the composer are: a input vector x, multiple hidden states h1, h2, . . . , hn and multiple memory cells c1, c2, . . . , cn, where n is the number of child units.

outputs consist of a memory cell c and a hidden state h which can be interpreted as the representation of a phrase.


2. Internal part.

controllers 和 memory of the composer.

controlling the flow of information by an input gate i, an output gate o and multiple forget gates f1, f2, . . . , fn.

转换等式如下：
![Child_Sum_Tree_LSTM][Child_Sum_Tree_LSTM]


### Child-Sum Tree-GRU

与 Tree-LSTM 机制 类似。 相比较于 Tree-GRU 移除了 memory cell c, 引入 updata gate z, 以及 multiple reset gates r1,r2,...,rn, 使 composer 能够 从 child units 的 hidden states 恢复(reset)。

转换等式如下：
![Tree_GRU_Structure][Tree_GRU_Structure]


## Attentive Tree-RNNs

将 Attention 与 Standard Tree-RNN 结合，主要从以下几方面考虑：
1. 在 Sentences pair modeling 任务中，两个句子会产生语意想关性。

2. 语意相关性的作用，可以通过 在构建 Sentence representation 时，赋予 each child 不同的权重。

3. attention mechanism 很适合与 学习一个 文本集合 的权重，用来指引 关注的向量。

### Soft Attention Layer
通过 一个 soft attention layer层来实现。

给定 一个隐藏状态集合：h1, h2,..., hn 和一个 外部向量 s. 权重计算方法如下：
![Soft Atte Eq][Soft_Atte_Eq]

### MLP

最后加上 MLP 层，用以学习高维组合特征，用以预测。


> pic

[Model_Structure]:05-pic/05-Tree_LSTM_Model_Structured.png
[Tree_RNNs_Structure]:05-pic/05-Tree_LSTM_Tree_RNNs_Structure.png
[Child_Sum_Tree_LSTM]:05-pic/05-Tree_LSTM_Child_Sum_Tree_LSTM.png
[Tree_GRU_Structure]:05-pic/05-Tree_LSTM_Tree_GRU_Structure.png
[Soft_Atte_Eq]:05-pic/05-Tree_LSTM_Soft_Atte_Eq.png


