import os
import jieba
import collections


# 读取指定文件夹路径下的所有文本文件内容
def read_txt(filepath):
    files = []
    contents = []
    for root, dirs, files in os.walk(filepath):
        for fName in files:
            file_path = os.path.join(root, fName)
            with open(file_path, encoding='utf-8') as f:
                content = ''.join(f.readlines())
                contents.append(content)
    return files, contents


def count(word_list, word_num=1):
    '''
    word_list:传入所需要预测往后词语的语料 list/str
    word_num:往后预测字/词的数量
    '''
    if word_list == '':
        return '', '', ''
    after_word = []
    c = 0
    if type(word_list) == list:
        i = 0
        max_length = len(dictionary)
        n = len(word_list)
        while i <= max_length - n:
            # print(i)
            j = 0
            loc = i
            while j < n:
                if dictionary[loc] == word_list[j]:
                    j = j + 1
                    loc = loc + 1
                else:
                    break
            if j == n:
                c = c + 1
                after_word.append(''.join(dictionary[loc:loc + word_num]))
            i = i + 1
    elif type(word_list) == str:
        dictionary_1 = ''.join(dictionary)
        i = 0
        while i != -1:
            i = dictionary_1.find(word_list)
            if i != -1:
                c += 1
                after_word.append(dictionary_1[i + len(word_list):i + len(word_list) + word_num])
                dictionary_1 = dictionary_1[i + len(word_list) + word_num:]
    counter = collections.Counter(after_word)
    return c, after_word, counter.most_common(1)[0][0]


if __name__ == '__main__':
    # 读取语料
    files, contents = read_txt(r'E:\5.工作\2024禾唱\输入法\语料')
    # 统计语料
    dictionary = ''.join(contents)
    # 去除标点符号
    stw = r"，。/；’：….？！【】[]"
    # 删除标点符号
    for n in stw:
        dictionary = ''.join(dictionary.split(stw))
    # 删除换行符
    dictionary = ''.join(dictionary.split('\n'))
    # 分词
    dictionary = jieba.lcut(dictionary)
    print('语料总长度为：', len(dictionary))

    while True:
        s = input('请输入要联想的单词或词组：')
        if s == 'exit':
            break
        num = input('请输入要联想的单词或词组的数量：')
        # 尝试将 num 转换为整数
        try:
            num = int(num)
        except ValueError:
            print('请输入一个有效的整数！')
            continue

        c, after_word, mostcommon = count(s, num)
        print('共出现', c, '次', s, '往后的词语为：', after_word, '出现次数最多的为：', mostcommon)
