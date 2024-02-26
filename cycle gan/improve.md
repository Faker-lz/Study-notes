# The Methods that improve cyclegan 



## 1 Cyclegan +  Attention

为了解决`Cyclegan`在域迁移任务中`区域识别`能力不足的问题，**[U-GAT-IT（ICLR：2020）](https://arxiv.org/pdf/1907.10830.pdf)**引入了新的**注意力机制**和**可学习的归一化函数（AdaLIN）**，使得模型能够更加有效地处理图像间的几何变换和纹理变换，缓解了cyclegan存在的**对齐问题**。

### 1.1 模型架构

![image-20240224170036652](improve.assets/image-20240224170036652.png)

该模型架构如上图所示，总体上采用**CycleGan**结构(模型图中只展开了对称的半部分)，包括生成器和鉴别器。在生成器和鉴别器中又采用了类似**VAE**结构，由**Encoder**和**Decoder**组成，同时在每个**Encoder**内部还有一个**Classifier**用于计算**Attention**的权重，与传统**VAE**结构不同的是，在特征提取和数据还原的过程中，模型采用了**残差神经网络**。

> 残差神经网络
>
> 其目的是为了解决深度学习模型中的**退化问题**(模型越深，拟合能力反而越差)，其直观上讲是将某些层的输出不经过后续的隐藏层，直接输入到目标层中(shortcut connection)，经典残差神经网络结构如下：
>
> ![残差神经网络（ResNet） - 知乎](https://pic4.zhimg.com/v2-fc3f5edf326a50b62f2bdacad24f035b_b.jpg)
>
> 简单来讲，在经过**shortcut connection**之后，模型在学习非线性变换的基础上也能学习线性变换，直接进行的shortcut connection相当于是进行了$y=x$的线性变换，理论上可以任意增加这样的线性变换层而模型的学习能力保持不变，这样就有效缓解了退化问题。
>
> 从梯度反向传播的角度来讲，在非常深的模型反向传播过程中，越靠近输入的浅层越可能受到中间某些层级较小梯度值的影响，当模型中间某一层的梯度接近于0时，浅层网络的参数无法得到有效的更新。但是在使用了残差结构之后，因为导数包含了恒等项，仍然能有效地进行反向传播。举一个非常直观的例子，假如有一个网络，输入$x=1$，非残差网络为$G$，残差网络为$H$，其中$H(x)=F(x) + x$，且有这样的输入关系：
>
> - 在$t$时刻，非残差网络$G_t(1)=1.1$，残差网络$H_t(1)=1.1, H_t(1)=F_t(1) + 1, F_t(1)=0.1$
> - 在$t+1$时刻，非残差网络$G_{t+1}(1)=1.2$，残差网络$H_{t+1}(1) = F_{t+1}(1) + 1, F_{t+1}(1)$=0.2
>
> 非残差网络和残差网络的梯度分别为：
>
> + **$\frac{d(G(x))}{x} =\frac{G_{t+1}(x) - G_{t}(x)}{G_t(x)}=\frac{0.1}{1.1}$**
> + **$\frac{d(F(x))}{x} =\frac{F_{t+1}(x) - F_{t}(x)}{F_t(x)}=\frac{0.1}{0.1}$**
>
> 可以看出变化对$F$的影响远远大于$G$，说明引入残差后的映射对于输出的变化更敏感，这样是有利于网络进行传播的。

#### 1.1.1 生成器

生成器首先通过**Encoder**（$E_s$）提取数据的$n$个特征映射，图中$E^k_s$表述数据的第$k$个特征映射；此外$\eta_s(x)$表示对应特征属于$x$的概率，$\eta(x)$受***CAM***的启发，辅助分类器学习第$k$个特征映射的权重$w^k_s$。在得到$E^k_s$和$w^k_s$后通过$a_s(x)=w_s * E_s(x)=\{w^k_s * E^k_s(x)\}$来计算对应的**attention matrix**。

> 何为CAM以及他的原理

之后通过***AdaLIN***方法计算$\gamma$和$\beta$参数:

![image-20240224172506875](improve.assets/image-20240224172506875.png)

其中$\mu_I$、$\mu_L$和$\theta_I$、$\theta_L$分别是**通道以及层的均值和标准差**

> 通道和层表示什么？以及AdaLIN的原理是什么？

#### 1.1.2 鉴别器

鉴别器的整体架构与生成器类似，都是采用**Encoder**和**Decoder**，此判别器与其他论文不同的点在于加入了$n_{D_t}(x)$判断 对应特征是来自原有数据还是生成数据，**attention matrix**$a_{D_t}(x)=w_{D_t} * E_{D_t}(x)$生成器计算方法类似。

### 1.2 损失函数

损失函数主要包含以下四个方面：

- `Gan`模型采用的经典的对抗性损失：与经典`Gan`模型的生成对抗性损失不同，该模型采用**最小二乘法计算损失**，使得生成器朝着目标域生成数据。
  $$
  L_{lsgan}^{s\to t}=(\mathbb{E}_{x\sim X_t}[(D_t(x))^2]+\mathbb{E}_{x\sim X_s}[(1-D_t(G_{s\to t}(x)))^2])
  $$
  

- 循环一致性损失：为了缓解可能存在的**模式坍塌**问题，以及确保进行域迁移前后的图片主体不变。

  $$
  L_{cycle}^{s\to t}=\mathbb{E}_{x\sim X_s}[|x-G_{t\to s}(G_{s\to t}(x)))|_1].
  $$
  

- 判别性损失：确保源图像和目标图像的**颜色**分布尽量一致。

  $$
  L_{identity}^{s\to t}=\mathbb{E}_{x\sim X_t}[|x-G_{s\to t}(x)|_1].
  $$

  > 是否会导致生成器生成一模一样的图片

- CAM损失：能够有效利用辅助分类器$\eta_s,\eta_{D_t}$，使得生成器和鉴别器学习到两种数据域最显著差异的区域，有助于模型的提升和训练

  $$
  \begin{gathered}L_{cam}^{s\to t}=-(\mathbb{E}_{x\sim X_s}[log(\eta_s(x))]+\mathbb{E}_{x\sim X_t}[log(1-\eta_s(x))]),\\\\L_{cam}^{D_t}=\mathbb{E}_{x\sim X_t}[(\eta_{D_t}(x))^2]+\mathbb{E}_{x\sim X_s}[(1-\eta_{D_t}(G_{s\to t}(x))^2].\end{gathered}
  $$
  
  
  > 具体原理

**完全的损失函数**：
$$
\min_{G_{s\to t},G_{t\to s},\eta_s,\eta_t}\max_{D_s,D_t,\eta_{D_s},\eta_{D_t}}\lambda_1L_{lsgan}+\lambda_2L_{cycle}+\lambda_3L_{identity}+\lambda_4L_{cam}
$$
其中$\lambda_1=1,\lambda_2=10,\lambda3=10,\lambda_4=1000$，而且$L_{lsgan} = L^{s\rightarrow t}_{lsgan} + L^{t \rightarrow s}_{lsgan}$并且其他三部分损失函数也都包含相互转换的两部分(与cyclegan类似)。

### 1.3 实验结果





