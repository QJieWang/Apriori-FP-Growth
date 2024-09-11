from Data import Data
from Apriori import DummyApriori
import sys
import os
if len(sys.argv) > 1:
    path = sys.argv[1]
    A = Data(path)
B = DummyApriori(A.data)
if len(sys.argv) > 2:
    support = float(sys.argv[2])
    B.set_support(support)
    # print('频繁项集为', B.ans_C)
if len(sys.argv) > 3:
    B.daxiangxiangji(int(sys.argv[3]))
    # Minc = float(sys.argv[3])
    # B.set_relateRules(Minc)

    # print('关联规则为:', B.relateRules)
