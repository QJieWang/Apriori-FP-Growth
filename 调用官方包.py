import pyfpgrowth
from Data import Data
A = Data("./第二次实践作业数据集/GroceryStore/Groceries.csv")
data = A.data
# 设置支持度和置信度
minS = 0.01
minC = 0.5
# 计算支持值
support = minS*len(data)
# 获取符合支持度规则数据
patterns = pyfpgrowth.find_frequent_patterns(data, support)
# 获取符合置信度规则数据
rules = pyfpgrowth.generate_association_rules(patterns, minC)
print(len(data))
print("获取符合支持度规则数据", patterns)
print("获取符合置信度规则数据", rules)
print(len(patterns))
print(len(rules))
