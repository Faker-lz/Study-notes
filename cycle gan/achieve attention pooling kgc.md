# Attention pooling achievement

## 1. 思路细化

![1197361cbda3c067ee82fe261adfdbb](achieve attention pooling kgc.assets/1197361cbda3c067ee82fe261adfdbb.jpg)

attention pooling函数**输入输出**：

- 输入：BERT encoding后的hr编码向量$V_{hr}(B * L * D)$和tail编码向量$V_t(B * L *D)$
- 输出：hr和tail的attention pooling向量，分别为$V'_{hr}(B * D)$和$V'_t(B * D)$

attention pooling函数**具体细节:**

- 先分别经过BERT encoder编码得到$V_{hr}(B * L* D)$和$V_t(B * L * D)$

- 根据mask获取到对应的有效token长度，$H$和$T$，裁剪对应的编码矩阵到相应的长度(为了方便后续计算这里仍保留矩阵的大小不变，对mask为0的token的embedding赋值为0)，即近似得到$V_{hr}(B * H * D)$和$V_t(B * T * D)$
- 对$V_t$向量的第二和第三维进行转置，得到$V_t^T(B * D * T)$
- 对$V_{hr}(B * L *D)$和$V_t^T(B * D * T)$进行批量矩阵相乘(bmm)，得到注意力矩阵$V_{a}(B * L * T)$
- 分别对$V_a$的第三和第二维度加和，得到注意力的和矩阵$V_a^{hr}(B * L)$和$V_a^t(B * E)$，之后对这两个矩阵第二维度进行$softmax$操作，得到最终的注意力权重矩阵$V_{attention}^{hr}(B * L)$和$V_{attention}^t(B * E)$
- 利用扩散机制对$V_{hr}(B * L * D)$和$V_{attention}^{hr}(B * L * (扩散到D))$进行元素相乘，得到计算的中间结果矩阵$V_{temp}(B * L *D)$，这样每个token的所有维度的embedding都乘上了相关的系数，最后沿着第二维度进行加和，对于$V_t(B * E * D)$和$V_{attention}^t(B * E)$进行类似的计算，得到最终的attention pooling向量$V_{hr}(B * D)'$和$V_t'(B * D)$

attention pooling 函数代码实现:

```python
import torch
import torch.nn.functional as F

def _pool_output(hr_output: torch.Tensor,
                 tail_output: torch.Tensor,
                 hr_mask: torch.Tensor,
                 tail_mask: torch.Tensor):
    # Masking the irrelevant parts of the input
    hr_output = hr_output * hr_mask.unsqueeze(-1)
    tail_output = tail_output * tail_mask.unsqueeze(-1)

    # Transpose tail_output for matrix multiplication
    tail_output = tail_output.transpose(1, 2)  # B * D * T

    # Perform batch matrix multiplication
    attention_matrix = torch.bmm(hr_output, tail_output)  # B * L * T

    # Compute attention weights
    attention_weights_hr = F.softmax(attention_matrix.sum(dim=2), dim=1)  # (B * L) Sum over T, softmax over L 
    attention_weights_tail = F.softmax(attention_matrix.sum(dim=1), dim=1)  # (B * T) Sum over L, softmax over T

    # Element-wise multiplication
    pooled_hr_output = hr_output * attention_weights_hr.unsqueeze(-1)
    pooled_tail_output = tail_output.transpose(1, 2) * attention_weights_tail.unsqueeze(-1)

    # Sum over the tokens to get the pooled output
    return pooled_hr_output.sum(1), pooled_tail_output.sum(1)

```



