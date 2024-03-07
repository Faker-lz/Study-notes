

## 总体结构 

![image-20240307162755890](introduction.assets/image-20240307162755890.png)

state：并不是单指actor的状态，而是环境中actor的状态

action:

observation：

environment：

episode：开始到整个结束的学习过程，包括所有的状态和动作以及得分，例如$\tau = \{s_1, a_1, r_1, s_2, a_2,  r_2 ... , s_t,a_t,r_t\}$(没有observation哦)

环境变化可能与action有关也可能无关



> 难点
>
> - 奖励延迟
> - agent探索

## 训练过程

![image-20240307164248881](introduction.assets/image-20240307164248881.png)

### 1.Actor行动选择器

以图像游戏为例，采用神经网络。

### 2.选择器好坏的衡量

$$
\bar{R_{\theta}} = \sum_{\tau}{R(\tau) \ P(\tau|\theta)} \\

P(\tau| \theta) = p(s_1)p(a_1|s_1, \theta)p(r_1, s_2 | a_1 , \theta)p(a_2|s_2, \theta)p(s_3,r_2 | a_2, \theta)...
$$

其中$R(\tau)$表示某种episode的Reward，$P(\tau|\theta)$表示这种episode在参数$\theta$下的期望，$\theta$为学习的参数，其核心思想是用每种可能性的期望来衡量选择器的好坏。

### 3.选择最好的选择器

将$\bar{R_\theta}$视为优化目标，通过反向传播优化参数$\theta$，其具体数学原理如下：

- 首先对整体的优化目标进行变形:$\bar{R_{\theta}} = \sum_{\tau}{R(\tau) \ P(\tau|\theta)} = $

反向传播

## 训练方法

 

![image-20240307162549975](introduction.assets/image-20240307162549975.png)

### Policy-based



### Value-based



### A3C





