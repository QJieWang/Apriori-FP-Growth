from Data import Data
import numpy as np
import pandas as pd


class DummyApriori(object):
    support = -1
    minC = -1    # 最小置信度
    data = None
    length = 0
    item = []
    C = {}
    Max = 0
    Min = 0
    turn = 0
    error = {}
    ans_C = {}    # 频繁项集
    relateRules = None  # 关联规则

    def __init__(self, data):
        self.data = data    # 通过Data类获得的数据
        self.sort_data()   # 数据排序
        self.length = len(data)    # 数据总数
        self.Min_Max(data)

        self.item = [i for i in range(self.Min, self.Max+1)]
        self.ans_C = {}    # 频繁项集
        self.temp_C = []
#         self.find_frequent_patterns()
#         freq_list = self.rulefromlist(self.ans_C)
#         self.calculate(freq_list, self.ans_C, self.minC)

    def set_support(self, support, method=1):
        """[summary]
            计算置信度，method可以取值[0,1,2,3]，其中0为未优化的方法，1，2，3为优化后的方法
        Args:
            support ([type]): [description]
            method (int, optional): [description]. Defaults to 2.

        Returns:
            [type]: [description]
        """
        if support == self.support:
            return None
        self.support = support
        self.ans_C = {}    # 频繁项集
        self.temp_C = []
        self.find_frequent_patterns(method)   # 创建平凡项集

    def set_relateRules(self, minC, support=support):
        if support != self.support:
            self.set_support(support)
        self.minC = minC
        freq_list = self.rulefromlist(self.ans_C)
        self.calculate(freq_list, self.ans_C, self.minC)

    def sort_data(self):
        self.data.sort()
        for i in self.data:
            i.sort()

    def Min_Max(self, data):
        Min = min(data[0])
        Max = 0
        for i in data:
            Max = max(Max, max(i))
            Min = min(Min, min(i))
        self.Max = Max
        self.Min = Min

    def find_frequent_patterns(self, method):
        self.ans_C = {}
        self.temp_C = []
        if method == 0:
            self.createC()
            while self.temp_C:
                # self.turn += 1
                # print(self.ans_C)
                # print("当前平凡项集的位数为", self.turn+1)
                self.createC()
        if method == 1:
            self.createC_1()
            while self.temp_C:
                # self.turn += 1
                # print(self.ans_C)
                # print("当前平凡项集的位数为", self.turn+1)
                self.createC_1()
        if method == 2:
            self.turn = 0
            self.data_copy = self.data.copy()
            self.data_index_dict = {i: 0 for i in range(len(self.data_copy))}
            self.turn += 1
            self.createC_2()
            while self.temp_C:
                self.turn += 1
                self.data_index_dict = {
                    i: 0 for i in range(len(self.data_copy))}
                self.createC_2()
        if method == 3:
            self.turn = 0
            self.data_copy = self.data.copy()
            self.data_index_dict = {i: 0 for i in range(len(self.data_copy))}
            self.turn += 1
            self.createC_3()
            while self.temp_C:
                self.data_index_dict = {
                    i: 0 for i in range(len(self.data_copy))}
                self.turn += 1
                self.createC_3()

    def createC(self):
        temp_D = []   # 下一个self.temp_C
        if not self.temp_C:
            self.temp_C = [[i] for i in self.item]      # 启动时，temp_C为空集
        for i in self.temp_C:
            # flag = True
            temp_sum = 0
            for j in self.data:
                if set(i).issubset(set(j)):
                    # flag = False
                    temp_sum += 1
                # else:
                #     if not flag:
                #         break
            self.error[str(i)] = temp_sum/self.length
            if temp_sum/self.length >= self.support:
                for k in range(i[-1]+1, self.Max+1):
                    temp_D.append(i+[k])
                self.ans_C[str(i)] = temp_sum/self.length
        self.temp_C = temp_D

    def jisuanzhichidu(self, a_list):
        temp_sum = 0
        for j in self.data:
            if set(a_list).issubset(set(j)):
                temp_sum += 1
        return temp_sum/self.length

    def createC_1(self):
        temp_D = []   # 下一个self.temp_C
        if not self.temp_C:   # 单元素的频繁项集
            self.temp_C = [[i] for i in self.item]      # 启动时，temp_C为空集
            for i in self.temp_C:
                zhichidu = self.jisuanzhichidu(i)  # 计算支持度
                if zhichidu >= self.support:
                    for k in range(i[-1]+1, self.Max+1):  # 生成新的待检查数组
                        temp_D.append(i+[k])
                    self.ans_C[str(i)] = zhichidu
        else:
            for i in self.temp_C:
                length = len(i)
                if str(i[0:length-2]+[i[length-1]]) in self.ans_C.keys() and str(i[0:length-2]+[i[length-2]]) in self.ans_C.keys():  # 检查父母字串是否符合要求
                    for k in range(i[-1]+1, self.Max+1):  # 生成新的待检查数组
                        temp_D.append(i+[k])
                    zhichidu = self.jisuanzhichidu(i)  # 计算支持度
                    if zhichidu >= self.support:
                        self.ans_C[str(i)] = zhichidu
        self.temp_C = temp_D

    def jisuanzhichidu_2(self, a_list):
        temp_sum = 0
        for j in range(len(self.data_copy)):
            if set(a_list).issubset(set(self.data_copy[j])):
                self.data_index_dict[j] += 1
                temp_sum += 1
        return temp_sum/self.length

    def remove_data_copy(self):
        temp = []
        biaozhun = self.length*self.support
        for i in range(len(self.data_index_dict)):
            if self.data_index_dict[i] < self.turn:
                temp.append(i)
        for i in temp[::-1]:
            del self.data_copy[i]

    def createC_2(self):
        temp_D = []   # 下一个self.temp_C
        if not self.temp_C:
            self.temp_C = [[i] for i in self.item]      # 启动时，temp_C为空集
        for i in self.temp_C:
            zhichidu = self.jisuanzhichidu_2(i)  # 计算支持度
            if zhichidu >= self.support:
                self.ans_C[str(i)] = zhichidu
                for k in range(i[-1]+1, self.Max+1):
                    temp_D.append(i+[k])
        remove_data_copy()
        self.temp_C = temp_D

    def createC_3(self):
        temp_D = []   # 下一个self.temp_C
        if not self.temp_C:   # 单元素的频繁项集
            self.temp_C = [[i] for i in self.item]      # 启动时，temp_C为空集
            for i in self.temp_C:
                zhichidu = self.jisuanzhichidu_2(i)  # 计算支持度
                if zhichidu >= self.support:
                    for k in range(i[-1]+1, self.Max+1):  # 生成新的待检查数组
                        temp_D.append(i+[k])
                    self.ans_C[str(i)] = zhichidu
        else:
            for i in self.temp_C:
                length = len(i)
                if str(i[0:length-2]+[i[length-1]]) in self.ans_C.keys() and str(i[0:length-2]+[i[length-2]]) in self.ans_C.keys():  # 检查父母字串是否符合要求
                    for k in range(i[-1]+1, self.Max+1):  # 生成新的待检查数组
                        temp_D.append(i+[k])
                    zhichidu = self.jisuanzhichidu_2(i)  # 计算支持度
                    if zhichidu >= self.support:
                        self.ans_C[str(i)] = zhichidu
        remove_data_copy()
        self.temp_C = temp_D

    def strtoist(self, stol):   # 将B.ans_C的键值变为int型变量
        s = stol[1:-1].split(",")
        ans = []
        for i in s:
            ans.append(int(i))
        return ans

    def rulefromlist(self, C_dict):   # 除了单个变量以外的频繁项集
        freq_list = []
        for i in C_dict.keys():
            temp = self.strtoist(i)
            if len(temp) > 1:
                freq_list.append(temp)
        return freq_list

    def calculate(self, freq_list, C_dict, min_C):
        def calculate_2(item, min_C, forward):
            if len(item) == 1:
                return None

            i = 0
            while i < len(item):
                temp_item = item.copy()
                temp_item.remove(item[i])
                temp_item.sort()
                if fenmu/C_dict[str(temp_item)] >= min_C:
                    ans[str(temp_item)+"->"+str(item[i])] = fenmu / \
                        C_dict[str(temp_item)]
                    calculate_2(temp_item, min_C, forward+str(item[i]))
                else:
                    not_need.append([forward+str(item[i])])
                i += 1
        not_need = []
        # min_C = slef.min_C
        # C_dict = self.ans_C
        ans = dict()

        for item in freq_list:
            fenmu = C_dict[str(item)]
            calculate_2(item, min_C, "")
        self.relateRules = ans

    def daxiangxiangji(self, n):
        # 打印三项集
        length = 0
        for i in self.ans_C:
            i = self.strtoist(i)
            if len(i) == n:
                print(i)
                length += 1
        print("{}项集一共有{}个".format(n, length))
