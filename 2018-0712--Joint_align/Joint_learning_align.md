# Natural Machine Translation by Jointly Learning to Align and Translate

参考：
https://www.cnblogs.com/naniJser/p/8900720.html
https://blog.csdn.net/WUTab/article/details/73657905


## 主要贡献

提出了一种方法，改进了 encoder-decoder 对于长文本表现差的缺点；通过 允许模型 automatically (soft-)serach for parts of source sentence that are relevant to predicting a target word,without having to form these parts as a hard segment explicitly.  

本文称这种方法为 (soft-)alignments.   The encoder–decoder model which learns to align and translate jointly.  更适合 长句子。

## 基础的 RNN Encoder-Decoder 框架

Encoder 输入一个句子，词向量序列； 转换成 向量c.
![RNN-encoder-decoder][RNN-encoder-decoder-1]
其中，h_t 是 time t 时刻的 隐藏向量; c 由 隐藏向量序列产生。

Decoder 用来训练 预测 next word y_t, 基于文本向量 c, 和已经预测的词向量{y_1,...,y_t-1};  换种说法就是，Decoder 定义了一种 概率分布计算方式：
![Decoder][Decoder]
![Decoder-2][Joint_align--Decoder-2.png]

## 本文中的 模型框架
![model_structure][model_structure]
### Learning to Align and Transflate

Decoder;
定义条件概率如下：
![new_Decoder][new_Decoder]

不同于一般的 encoder-decoder模型，每个word y_i 的概率与 context vector c_i 直接相关。

c_i 是由 annotations h_i 的加权和计算而来。
![c_i][c_i]
权重计算方式如下:
![atte_cpt][atte_cpt]  s_i  是 (decoder)RNN 在时刻 t 的隐藏状态。 h_i 是 encoder 编码后对应input的向量序列。

soft-align 就体现在 e_ij 的计算上。 用以衡量 输入序列中 i位置 和 输出序列中 j位置 的匹配程度。

Encoder;
利用 BiRNN 提取input seq的双向信息。 每个隐藏状态 h_i 包含 该词前后的语境信息。







> pic

[RNN-encoder-decoder-1]:pic/Joint_algin--RNN-encoder-decoder-1.png
[Decoder]:pic/Joint_align--Decoder.png
[Decoder-2]:pic/Joint_align--Decoder-2.png

[new_Decoder]:pic/Joint_align--new_Decoder.png
[c_i]:pic/Joint_align--c_i.png
[atte_cpt]:pic/Joint_align--atte_cpt.png
[model_structure]:pic/Joint_align--model_structure.png

