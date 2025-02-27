import gurobipy as gp
from gurobipy import GRB
import numpy as np
import matplotlib.pyplot as plt
# 从模型中获取变量
def get_vars(model,name):
    vars = model.getVars()
    dict = {}
    for v in vars:
        parts = v.VarName.replace('[', ' ').replace(']', ' ').split()
        if parts[0] == name:
            try:
                dict[parts[1]] = v.X
            except:
                dict = v.X
    return dict

# 获取 gurobi 变量的值
def get_values(x):
    if isinstance(x, gp.tupledict):
        return np.array([v.X for v in x.values()])
    else:
        return x.X

def get_values_dict(x,attrname = GRB.Attr.X):
    if isinstance(x, gp.tupledict):
        return gp.tupledict({k:v.getAttr(attrname) for k,v in x.items()})
    else:
        return x.getAttr(attrname)

# 绘制一维数据的图像
def plot_values(x):
    name = x[0].VarName.split(sep='[')[0]
    x_values = get_values(x)
    plt.plot(range(len(x_values)), x_values)
    plt.title(f'{name}')
    plt.show()
