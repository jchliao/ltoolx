# Introduction

L2的妙妙工具包，包含gurobi、matplot相关函数。

## Matplotlib tools

提供更为强大的svg矢量图导出功能，完整功能需要结合axisartist使用。
在plot选项当中添加`gid="out"`参数，将折线线段化，并剔除超出坐标轴的图线，实现图像在ppt、visio等工具当中的更多编辑功能。

使用示例如下：

```python
from ltoolx.matplotlib_utils import *
from ltoolx.svg_utils import *
import mpl_toolkits.axisartist as AA
# plt直接使用方法
plt.axes(axes_class=AA.Axes)
plt.plot([1, 2, 3], [3, 5, 4], label="inax", marker="s")
plt.plot(
    [1, 2, 3], [5, 15, 3], gid="out", label="outax", linestyle="--", marker="o"
)
plt.xlim([1.25, 3])
plt.ylim([4.0, 10.0])
plt.legend()
savefig("test1.svg")

# 创建figure对象使用方法
fig= plt.figure()
ax = fig.add_subplot(axes_class=AA.Axes)
ax.plot([1,2,3],[3,2,4],label='inax')
ax.plot([1,2,3],[5,15,3],label='outax',gid='out')
ax.set_ylim([0,10])
ax.legend()
Fig(fig).savefig("test2.svg")

```

## 导出为vsd并保存到剪切板

```python
from ltoolx.matplotlib_utils import *
from ltoolx.svg_utils import *
# plt直接使用方法
plt.plot([1, 2, 3], [3, 5, 4], label="inax", marker="s")
plt.plot(
    [1, 2, 3], [5, 15, 3], gid="out", label="outax", linestyle="--", marker="o"
)
plt.xlim([1.25, 3])
plt.ylim([4.0, 10.0])
plt.legend()
savefig("test1.svg").to_vsd(clipboard=True)

# 创建figure对象使用方法
fig= plt.figure()
ax = fig.add_subplot(axes_class=AA.Axes)
ax.plot([1,2,3],[3,2,4],label='inax')
ax.plot([1,2,3],[5,15,3],label='outax',gid='out')
ax.set_ylim([0,10])
ax.legend()
Fig(fig).savefig("test2.svg").to_vsd(clipboard=True)

```