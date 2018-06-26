# Joint Copying and Restricted Generation for Paraphrase

## 主要内容

主题： Paraphrase 释义。  Seq2Seq model, called CoRe.

方法： 
    结合 2 种方式来综合释义：copying decoder, restricted generative decoder. 其中，copy decoder 基于 attention model; generative decoder 基于 source-specific vocabulary.  利用一个 predictor(分类器，预测器) 来选择copying 或者 rewriting两种模式。


模型架构图：
![Model Structure][Model_Structure]


## 贡献
• We develop two different decoders to simulate major human writing behaviors in paraphrase.
• We introduce a binary sequence labeling task to predict the current writing mode, which utilizes additional supervision.
• We add restrictions to the generative decoder in order to produce highly relevant content efficiently.


### two different decoders

1. Copying Decoder

Attention mechanism gives us the copying probability distribution for the learned alignment.

The copying decoder reduces the chance to produce the UNK tags.

2. Restricted Generative Decoder

涉及到 alignment table A.  限制 vocabulary V 的size.


### binary sequence labeling task  current writing mode

监督学习，用来结合两种 decoder, 抉择选择哪种 decoder 模式。

### restrictions to the generative decoder

涉及到 alignment table A.  限制 vocabulary V 的size.


> pic

[Model_Structure]:04-pic/04--Paraphrase_Model_Structure.png
