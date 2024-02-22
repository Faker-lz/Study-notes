# The Log-Sum-Exp Trick

**在查看torch中的BCEWithlogits文档时注意到有使用`log-sum-exp（LSE）`技巧来提高计算结果的数值稳定性，学习后进行记录。**

**归一化log概率是统计模型中常见的一类任务，但是在使用指数运算较大的值的时候可能会导致数据溢出（上溢或者下溢）。有一种叫做log-sum-exp的技巧来解决这个问题。**

___

在统计模型和机器学习中，经常会使用到log来计算，这是因为log有许多很好的性质，比如，在计算多个概率乘积时，如果直接计算$x*y$可能会导致下溢，这时就可以使用log将线性空间的乘法转化为对数空间的加法，如公式(1)，同时为了方便，在计算过程中的概率都是以对数形式存储的，也就是$e_x$和$e_y$：

$$log(xy) = log(x) + log(y)=e_x + e_y\tag{1}.$$

此外，log在处理函数相乘的线性微分时，可以把乘法的微分转化为对分别微分再做加法，通常来讲单个函数的微分是要比运用乘法法则计算的微分更加容易：

$$\frac{\alpha}{\alpha_x}log[f(x)g(x)]=\frac{\alpha}{\alpha_x}log(f(x)) + \frac{\alpha}{\alpha_x}log(g(x)) \tag{2}.$$

这只是两个十分浅显的使用log运算的好处，此外，用log在数值稳定性上有着非常好的性质，以至于很多标准库都在用它计算概率密度函数(PDFs)。

然而很多时候，需要对数据进行log的逆运算。比如在使用$softmax$函数归一化概率向量$N=(x_1,x_2,...,x_n), x_i=log(p_i)$时：

$$p_i=\frac{exp(x_i)}{\sum_{n=1}^N exp(x_n)}, \sum_{n=1}^N=1.\tag{3}$$

由于$x_n$是log计算后的概率，它的值可能非常小，经过指数运算之后可能产生下溢的结果(等于0)。对$softmax$经过简单变换可得：

$$exp(x_i)=p_i\sum_{n=1}^Nexp(x_n) \\ x_i=log(p_i) + log(\sum_{n=1}^Nexp(x_n))\\log(p_i)=x_i-log(\sum_{n=1}^Nexp(x_n)).$$

可以看到在计算$softmax$ 过程中出现了$LSE$：

$LSE(x_1, x_2,...,x_n)=log(\sum_{n=1}^Nexp(x_n)).$

可以证明$LSE$能够解决上文提到的上溢或者下溢的问题：

$y=log(\sum_{n=1}^Nexp(x_n))\\ e^y = \sum_{n=1}^Nexp(x_n) \\ e^y=e^c\sum_{n=1}^Nexp(x_n-c)\\y=c+log(\sum_{n=1}^Nexp(x_n-c)).$

可以看出，如果将$LSE$指数中的所有数移动任意值，其结果仍会保持不变。令$c=\max\{x_1,x2,...,x_n\}$就能确定最大的指数项为1，可以避免溢出情况的发生。



## 代码示例

首先，令$x_n$为足够大且会导致溢出。

```python
>>> x = np.array([1000, 1000, 1000])
>>> np.exp(x)
array([inf, inf, inf])
```



 







