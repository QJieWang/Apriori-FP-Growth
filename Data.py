import pandas as pd
import pickle


class Data(object):
    """[summary]
    读取处理数据
    Args:
        object ([type]): [description]

    Returns:
        [type]: [description]
    """
    file = None
    item_dict = None   # 字典数据
    item_con = None    # 置信度字典
    key_list = None   # 按照执行都排序后的物品名
    values_list = None     # 按照置信度排序后的物品置信值
    length = None    # 商品数量
    correspond_dict = None    # 文件名的转换规则
    data = None  # 数据结构

    def __init__(self, filename):
        """
        初始化读取文件
        Args:
            filename([object]): [文件名]
        """
        self.file = pd.read_csv(filename)
        # self.file = pd.read_csv("./第二次实践作业数据集/GroceryStore/Groceries.csv")
        self.number_items(self.file)
        self.confidence(self.item_dict)
        a, b = self.dict_sort(self.item_con)
        self.gennerate_item_list(self.file)
        self.save_data()

    def gennerate_item_list(self, file):
        """[summary]
        生成对应的数据结构
        Args:
            file([type]): [description]文件名

        Returns:
            ans  文件数据
            correspond_dict   对应转换规则
        """
        ans = []
        correspond_dict = {}
        index = 0
        temp = dict()
        for item in file["items"]:
            temp_list = []
            string = item[1:-1]
            strlist = string.split(",")
            for j in strlist:
                if j in correspond_dict:
                    temp_list.append(correspond_dict[j])
                else:
                    index += 1
                    correspond_dict[j] = index
                    temp_list.append(correspond_dict[j])
            ans.append(temp_list)
        self.data = ans
        self.correspond_dict = correspond_dict
        return ans, correspond_dict

    def number_items(self, file):
        """[summary]
        用来统计文本中包含的所有事务种类以及对应的频率，方便进行规则提取
        Args:
            file([pd对象]): [文件]
        """
        temp = dict()
        for item in file["items"]:
            string = item[1:-1]
            strlist = string.split(",")
            for i in strlist:
                if i in temp:
                    temp[i] += 1
                else:
                    temp[i] = 1
        self.item_dict = temp
        self.length = len(temp)

    def confidence(self, item_dict, number=9835):
        """[summary]
        计算置信值
        Args:
            item_dict([type]): [description]物品字典：其中键为物品名称，键值为商品在数据库中出现的次数
            number(int, optional): [description]. Defaults to 9835.数据库总条书，本次实验默认数据为9835条

        Returns:
            [type]: [description]
        """

        Max = max(item_dict.values())
        Min = min(item_dict.values())
        number = 9835   # 这里的number是所有的
        item_con = dict()
        for key in item_dict.keys():
            item_con[key] = item_dict[key]/number
        self.item_con = item_con

    def dict_sort(self, item_con):
        """[summary]
        按照度排序, 并返回列表
        Args:
            item_con([type]): [物品字典]

        """
        # '''
        # 对类进行排序
        # item_con  待排序字典
        # return：
        # key_list    排序后的物品名称
        # values_list    排序后的物品value值
        # '''
        key_list = sorted(item_con, key=lambda item: item_con[item])
        values_list = sorted(item_con.values())

        self.key_list = key_list
        self.values_list = values_list
        return key_list, values_list

    def save_data(self):
        """[summary]
        保存数据
        """
        with open('data.pk', 'wb') as file:
            pickle.dump(self.data, file)
        file.close()

    def load_data(self, filename="data.pk"):
        """[summary]
        加载数据
        Args:
            filename([type]): [description]文件地址
        """
        with open(filename, 'rb') as file:
            temp = pickle.load(file)
        file.close()
        return temp


class Utile(object):
    def __init__(self):
        pass

    def save_data(self):
        """[summary]
        保存数据
        """
        with open('data.pk', 'wb') as file:
            pickle.dump(self.data, file)
        file.close()

    def load_data(self, filename="data.pk"):
        """[summary]
        加载数据
        Args:
            filename([type]): [description]文件地址
        """
        with open(filename, 'rb') as file:
            temp = pickle.load(file)
        file.close()
        return temp

    def json_data(self):
        """[summary]
        将对应关系字典生成为JSON文件并保存
        Args:
            data([type], optional): [description]. Defaults to self.correspond_dict.
        """
        data = self.correspond_dict
        with open("对应关系.json", "w", encoding='utf-8') as f:
            json.dump(correspond_dict, f, indent=2,
                      sort_keys=True, ensure_ascii=False)  # 写为多行
            f.close()
        print("Json 对应文件生成完毕")
