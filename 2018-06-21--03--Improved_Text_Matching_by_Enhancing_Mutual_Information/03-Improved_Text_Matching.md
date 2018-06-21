# Improved Text Matching by Enhancing Mutual Information

## 主要内容

主题：Text Matching,

应用领域：QA(question answering), IR(information retrieval).

关键词： reformulate (重建，重构), [重构方法：generative adversarial network(生成对抗网络) ]
reformulate( GAN对抗生成网络 ), 作用目标：使 生成的问题 与 原问题 在嵌入空间(embedding space)相似.

GAN 生成文本的主要问题：non-differentiability of discrete text.(离散文本的不可区分性)
解决方案：policy gradients，更新训练参数。


数据集：zhihu, SemEval, WikiQA;


## 相关工作

something...

## 本文方法

### Question Rewriting

1. GAN(Goodfellow etal. 2014); 
主要有两部分组成： generator G(x;sita_g) 和 discriminator D(y;sita_d) ;
目标： 通过训练一个无监督深度生成模型，使其能够生成一个与 原真实样本 相似的 样本；

解释下： G 是生成器，D 是鉴别器。 通过训练迭代，达到平衡，G生成的样本迷惑D，D不能正确识别是否为生成的样本。


GAN的优化目标函数 V(D,G)：
![GAN Objective][GAN_Objective]

y = G(x; sita_g); 样本x通过生成器G生成样本y;
目标函数对于G，maxmize D犯错误的可能性；
对于D，try best to 正确分类。

具体来讲:一方面，G想要迷惑D，使D将生成样本y当做真实样本，即D(y)~1(real); 另一方面,D需要尽可能的正确分类y,即 D(y)~0(fake), D(x)~1(real);
由上述规则，参数 sita_g, sita_d 更新策略如下：
![Param Optimizer][Param_Optimizer]

For text generation, however, y consists of discrete words and is no more differentiable w.r.t. θg since y is the outcome of argmax function, which is non-differentiable.
(这句没太理解。。。先留着坑，以后知识储备再来填坑~)

2. Generating Model (生成模型)
生成模型部分架构图：
![Generator Model][Generator_Model]

Encoder--输入部分：一个句子，词序列。 利用 attention机制，Bi-RNN 模型对 词序列编码，直接学习attentivede 句子表征 C_t。

Decoder--生成句子部分：RNN_dec，用来评估 预测词 与 C_t(原句子表征) 的联合概率。
![Joint Probability][Joint_Probability]

对于每一个预测词 y_t, RNN_dec 输出一个概率分布 p_t/in R^V(V是词典大小)，计算如下所示:
![Probability Distribution][Probability_Distribution]

其中，s_t 是 RNN_dec 第t步的隐藏层输出，C_t 是原句子表征。计算方式如下：
![C_t Computation][C_t_Computation]


3. Policy Gradients Training

尽管 p(y_t|y<t,x) 关于 生成参数 sita_g 是可区分的。但是经过 argmax后的y_t 却不可区分；于是，Eq.2 中的关于 参数 sita_g 的 梯度 将为0，sita_g 将不会更新。
Policy Gradients 常常用在强化学习任务中，来解决这种问题。
在这里，将 生成网络 G 当做一个 policy network, 损失函数如下：
![G PolicyNet Obj][G_PolicyNet_Obj]
其中，Q(y)是 action-value function;the reward for gen- erating sequence y.
G(y|x) 基于policy network评估 基于输入句子x 生成序列y的可能性。
因为，G 需要 迷惑 D,即 maximize D(y). 令 Q(y) = log(1-D(y)), 即 maximize D(y) ==> minimize L;
在 Eq.8 中， y是独立于 sita_g 的， 因此，Delt_{sita_g} Q(y) = Delt_{sita_g} log(1-D(y)), 因此有：
![Gradient sita_g][Gradient_sita_g]
因为 G 需要 maximize D(y) 或者 minimize L, 生成器参数 sita_g 可以通过下式更新：
![sita_g Update][sita_g_Update]

4. Augmented Mutual Information

Q, A 之间互信息计算公式：I(Q,A) = H(A) - H(A|Q) = H(Q) - H(Q|A) ; 如果 A = f(Q)， 则有，H(Q|A)=H(A|Q) = 0; 即 I(Q,A)最大化。

然后，如果 给定 一个 fixed matching model, 如果能产生一个 new question Q_2, 则 A 不确定性被缩小了：H(A|Q_1,Q_2) < H(A|Q_1); 即有：I(Q_1, Q_2, A) = H(A) - H(A|Q_1, Q_2) > H(A) - H(A|Q_1) = I(Q_1, A)

因此，通过重写一个新的问题，丰富了互信息。



### Matching Model

1. Encoding and Matching

采取 共享权重的 Bi-GRU 对两个句子 q_o, q_r 编码， Bi-GRU 对 answer 编码。 Bi-GRU 中，对每一个时间步的输出，当做当前词的编码，然后将双向相同词编码，进行concat，则可以将 词向量序列 看做一个矩阵。
F = tanh( F` ) = tanh( QWA^T ) ; 这样就将 Q,A 编码为一个矩阵F。然后，再利用 CNN 提取矩阵 F 中的重要特征，Flatten后，进入Dense层，然后就可以最终得到预测分数。


### Ranking Function

预测排序序列 o_1, o_2,...,o_M 由 relevance scores s_1,s_2,...,s_M 得到。例如：如果 M=5, ground truth order 为 (2,5,1,3,4), predicted scores 为 (0.3, 0.6, 0.4, 0.2, 0.7); 那么最终预测序列(越大越好)为 (2, 4, 3, 1, 5); 为了有效评估最终的预测序列好坏，采用 LambdaRank 算法计算rank loss, the probability that answer A_i is permuted(置换) ahead of A_j is defined as:
![Prob Rank][Prob_Rank]
对于 A_i 和 A_j 的损失函数定义为：
![Loss Rank][Loss_Rank]

则，由Eq.14,Eq.15,可得最终的损失函数计算公式为：
![Loss Rank final][Loss_Rank_final]
其中，S_{ij} = sign( l_i - l_j ). 假设 sita 为 模型参数，则 sita 关于 L 的梯度为：
![Gradient sita][Gradient_sita]
其中，![Lambda_ij][Lambda_ij], ![Final Lambda_i][Final_Lambda_i]

> 这块损失计算，没咋看懂。有点蒙，有时间再仔细研究下。

### 实验部分

实验部分，还未研究。

待续。。。



 pic:  

[GAN_Objective]:03-pic/03--Text_match_GAN_Obj.png
[Param_Optimizer]:03-pic/03--Text_match_Param_Optimizer.png
[Generator_Model]:03-pic/03--Text_match_Generator_Model.png
[Joint_Probability]:03-pic/03--Text_match_Joint_Probability.png
[Probability_Distribution]:03-pic/03--Text_match_Prob_Distrib.png
[C_t_Computation]:03-pic/03--Text_match_C_t_Computation.png
[G_PolicyNet_Obj]:03-pic/03--Text_match_G_PolicyNet_Obj.png
[Gradient_sita_g]:03-pic/03--Text_match_Gradient_sita_g.png
[sita_g_Update]:03-pic/03--Text_match_sita_g_Update.png
[Prob_Rank]:03-pic/03--Text_match_Prob_Rank.png
[Loss_Rank]:03-pic/03--Text_match_Loss_Rank.png
[Loss_Rank_final]:03-pic/03--Text_match_Loss_Rank_final.png
[Gradient_sita]:03-pic/03--Text_match_Gradient_sita.png
[Lambda_ij]:03-pic/03--Text_match_lambda_ij.png
[Final_Lambda_i]:03-pic/03--Text_match_Final_lambda_i.png


