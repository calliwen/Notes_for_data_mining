#  (BMP)  Bilateral Multi-Perspective Matching for Natural Language Sentences

参考：https://zhuanlan.zhihu.com/p/26548034

Natural language sentence matching ( NLSM ) 自然语言句子匹配，比较两个句子并判断句子建关系，是许多任务的一项基本技术。
两种流行的深度学习框架：
（1）Siamese network：对两个句子通过同样的神经网络结果，得到两个句子向量，然后对这两个句子向量做匹配。共享采参数，能有效减少学习的参数。缺点：只针对两个句子向量做匹配，缺少两个句子的交互信息。
（2）Matching-aggregation:先对两个句子之间的单元做匹配，匹配的结果通过一个神经网络（CNN & LSTM）聚集为一个向量后做匹配。捕捉了两个句子建的交互特征。缺点：只是基于词级别忽略了其他层级的信息。匹配只是基于一个方向忽略了相反的方向。

为了解决 matching-aggregation 框架的不足，该文章提出了一种双向的多角度匹配模型(bilateral multi-perspective matching)。该模型 在 同义识别、自然语言推理、答案选择任务上都取得了较好的结果。

整体架构图如下：

![model structure][nlsm-structure]

Word Representation Layer:两种输入， 词向量(word emb)， 字向量(char emb);

Context Representation Layer: 将上下文信息融合到 P和Q每个时间步(time-step)的表示中，这里利用了 Bi-LSTM 结构。

Matching Layer:
双向：比较 句子P的每个上下文向量(time_step)和句子Q的所有上下文向量(time-step)。

Prediction Layer: 预测概率Pr(y|P,Q), 利用两层前馈神经网络然后接 softmax分类。

其中，多角度匹配(Multi-perspective Matching)，可以分为以下四种方案：
![Multi Perspective Matching][multi-perspective-matching]

首先定义一下权重向量计算方式；
m = f_m(v1,v2; W) ;  m = [m_1, m_2,...,m_k]; 
m_k = cosine( W_k * v1, W_k * v2 )    W_k 是 W 矩阵的 第 k 行；

然后，为了比较一个句子的某个 time-step 和 另一个句子的所有 time-step，制定了四种匹配策略。 以下仅从单向进行描述，例 从 P 到 Q .

(1) Full-Matching
取一个句子的某个 time-step 和另一个句子的最后一个 time-step 进行比较计算。
![Full Matching][Full-matching]
简单理解就是，两个向量通过计算得到一种角度下的 一个向量( m_i )。 然后再考虑每个时间步( time-step )； 及最后经过处理后，得到两个  词向量序列（包含互信息）。

(2) Max-Pooling Matching
取一个句子的某个 time-step 和 另一个句子的所有 time-step 比较后取最大。
![Max Pooling Matching][Max-Pooling-Matching]
简单理解就是，Full-matching版本的强化。 例如，P 和 Q 之间，取 P 的某个time-step, 与 Q 的所有时间步进行比较，然后取对应 维度上的最大值。最后的 shape 仍然和 (1) 中的一样，只是考虑 P 中某一时间步与 Q 整体的信息。

(3) Attention-Matching
首先计算一个句子的某个 time-step 和另一个句子的 所有 time-step 的余弦相似度。
然后利用余弦相似度对另一个句子的所有 time-step 加权取平均。
![atte-matching-1][atte-matching-1]
![atte-matching-2][atte-matching-2]
由以上两个步骤，可以得到两个 Attention(加权平均)后的 两个词向量序列；
![atte-matching-3][atte-matching-3]

注意， h_i^{mean} 是 P 中 第 i 个 time-step 向量与 Q 中所有 time-step 的attention后的加权平均。所以，h_i^{mean} 也是 P 中的中的一个 词向量序列。
故 在 eq9中，得到的 m_i^{att} 也是一个 词向量序列(矩阵)。

(4) Max-Attentive-Matching
与(3) 中方法类似，只是 加权平均过程变为了按 特征维度，取最大。

小结：
上述论文中的方法，最后处理后的输出仍是 两个 词向量序列(矩阵). 只是 每个句子的每个时间步都包含另一个句子的各时间步的信息。 考虑额互信息。



> pic

[nlsm-structure]:02-pic/nlsm-structure.png
[multi-perspective-matching]:02-pic/BIMPM--multi-perspective-matching.png
[Full-matching]:02-pic/BIMPM--Full-matching.png
[Max-Pooling-Matching]:02-pic/BIMPM--Max-Pooling-Matching.png
[atte-matching-1]:02-pic/BIMPM--atte-matching-1.png
[atte-matching-2]:02-pic/BIMPM--atte-matching-2.png
[atte-matching-3]:02-pic/BIMPM--attention-matching-3.png


