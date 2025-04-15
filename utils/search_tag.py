import re
import pandas as pd
import copy
from fuzzychinese import FuzzyChineseMatch

class SearchTag:
    def __init__(self, csv_path='./utils/danbooru.csv'):
        self.csv_path = csv_path
        self.df = None
        self.df_raw = None
        self.cn_raw_name = None
        self.tag_dict = None
        self.fcm = None
        self._initialize()

    def _initialize(self):
        # 读取 CSV 文件
        self.df = pd.read_csv(self.csv_path, on_bad_lines='skip')
        self.df_raw = copy.deepcopy(self.df)

        # 清洗 tag_cn 列：保留中英文混合内容，但去除空值
        self.df['tag_cn'] = self.df['tag_cn'].apply(lambda x: x.strip() if pd.notna(x) else '')  # 去除空白字符
        self.cn_raw_name = dict(zip(self.df['tag_cn'], self.df_raw['tag_cn']))
        self.df = self.df[self.df['tag_cn'] != '']  # 去除空字符串

        # 将 tag_cn 列作为字典的键，tag 列作为字典的值
        self.tag_dict = dict(zip(self.df['tag_cn'], self.df['tag']))

        # 初始化 FuzzyChineseMatch
        self.fcm = FuzzyChineseMatch(ngram_range=(3, 3))

        # 训练模型，传入纯中文部分作为目标词典
        chinese_only_tags = self.df['tag_cn'].apply(self.extract_chinese)
        self.fcm.fit(chinese_only_tags[chinese_only_tags != ''])  # 仅传入非空的中文部分

    @staticmethod
    def extract_chinese(text):
        """提取文本中的纯中文部分"""
        return ''.join(re.findall(r'[\u4e00-\u9fff]', text))

    def search_tag(self, text):
        # 判断输入是中文还是英文
        if re.search(r'[\u4e00-\u9fff]', text):  # 如果包含中文字符
            # 1. 全字匹配（完全一致）
            exact_matches = self.df[self.df['tag_cn'] == text]['tag_cn'].tolist()
            # 2. 部分匹配（部分内容一致，按匹配位置靠前的优先）
            partial_matches = self.df[self.df['tag_cn'].str.contains(text, case=False, na=False)]['tag_cn'].tolist()
            # 3. 提取中文部分进行模糊匹配
            chinese_part = self.extract_chinese(text)
            if chinese_part:  # 如果有中文部分
                fuzzy_matches = self.fcm.transform(pd.Series([chinese_part]), n=20)[0]
            else:
                fuzzy_matches = []
        else:  # 如果是英文
            # 1. 全字匹配
            exact_matches = self.df[self.df['tag'].str.lower() == text.lower()]['tag_cn'].tolist()
            # 2. 全词匹配（匹配位置靠前的优先）
            partial_matches = self.df[self.df['tag'].str.contains(r'\b' + re.escape(text) + r'\b', case=False, na=False)]['tag_cn'].head(40).tolist()
            # 3. 模糊匹配（基于英文部分）
            fuzzy_matches = []

        # 合并全字匹配、部分匹配和模糊匹配的结果，并去重
        all_matches = list(set(exact_matches + partial_matches + list(fuzzy_matches)))

        # 对匹配结果进行排序：全字匹配 > 全词匹配（按匹配位置） > 模糊匹配
        sorted_matches = sorted(all_matches, key=lambda x: self.get_match_priority(x, text))

        # 构建结果字符串
        result = f"输入的文本: {text}\n匹配结果：\n"
        for i, matched_key in enumerate(sorted_matches, start=1):
            if matched_key in self.tag_dict:
                result += f"{i}. {self.cn_raw_name[matched_key]} => `{self.tag_dict[matched_key]}`\n"
        return result

    def get_match_priority(self, matched_key, text):
        """
        计算匹配优先级：
        1. 全字匹配优先级最高
        2. 全词匹配时，匹配内容越靠前优先级越高
        3. 模糊匹配优先级最低
        """
        if re.search(r'[\u4e00-\u9fff]', text):  # 如果包含中文字符
            if matched_key == text:
                return 0  # 全字匹配优先级最高
            elif text in matched_key:
                return matched_key.find(text) + 1  # 部分匹配按位置排序
            else:
                return 1000  # 模糊匹配优先级最低
        else:  # 英文匹配
            tag_value = self.tag_dict[matched_key]
            if tag_value.lower() == text.lower():
                return 0  # 全字匹配优先级最高
            elif re.search(r'\b' + re.escape(text.lower()) + r'\b', tag_value.lower()):
                return tag_value.lower().find(text.lower()) + 1  # 全词匹配按位置排序
            else:
                return 1000  # 模糊匹配优先级最低

# 使用示例
if __name__ == "__main__":
    search_tag_instance = SearchTag()
    while True:
        text = input("输入要查询的TAG中文名或英文名：")
        result = search_tag_instance.search_tag(text)
        print(result)