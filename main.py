import re
from sklearn.feature_extraction.text import CountVectorizer


# encoding=utf-8
# 加载目的路径的文件
def dataLoad(path):
    try:
        with open(path, encoding='utf-8') as f:
            r = f.readlines()
    except FileNotFoundError:
        print(f"文件 {path} 未找到")
        return []

    # 用正则表达式匹配删除语料中无用的词性标注和符号
    pattern_clean = r'[0-9\-/[\]a-zA-Z\s]+'
    review1 = [re.sub(pattern_clean, '', txt) for txt in r]

    # 按照标点符号分出子句
    pattern_split = r'[.,;?!，“”‘’！…——()《》]'
    review2 = (re.split(pattern_split, txt) for txt in review1)
    review3 = [item.strip() for sublist in review2 for item in sublist if item.strip()]

    return review3


# # 2-gram输入联想函数，input_words为用户输入的单个字，返回联想的前num个结果的列表
def gram2(voc, input_words, freq_list, num=1):
    word2dict = {}
    flag = False
    for g2 in voc:  # 在所有两个字的组合中查找第一个字与用户输入字相同的组合
        if g2[0] == input_words:
            flag = True
            index = voc[g2]
            freq = freq_list[index]  # 获取该组合出现的频数，加入结果字典
            word2dict[g2] = freq
    if not flag:
        print('很抱歉，受当前语料库大小限制，无法进行联想。')
        return
    sort_word2 = sorted(word2dict.items(), key=lambda x: x[1], reverse=True)  # 降序排序
    if num <= len(sort_word2):
        output = sort_word2[0:num]
    else:
        output = sort_word2
    words2 = [i[0] for i in output]
    words = [i[2] for i in words2]
    r = [input_words + i for i in words]
    print('2-gram联想结果为：', r)
    return r


# 3-gram输入联想函数，input_words为用户输入的≥2个字，返回联想的前num个结果的列表
def gram3(voc, input_words, freq_list, num=1):
    seg = input_words[-2:]
    nseg = ' '.join(list(seg))
    word3dict = {}
    flag = False
    for g3 in voc:  # 在所有两个字的组合中查找第一个字与用户输入字相同的组合
        if g3[0:3] == nseg:
            flag = True
            index = voc[g3]
            freq = freq_list[index]  # 获取该组合出现的频数，加入结果字典
            word3dict[g3] = freq
    if not flag:
        final_word = input_words[-1]
        result1 = gram2(final_word, num)
        return result1
    sort_word3 = sorted(word3dict.items(), key=lambda x: x[1], reverse=True)  # 降序排序
    if num <= len(sort_word3):
        output = sort_word3[0:num]
    else:
        output = sort_word3
    words3 = [i[0] for i in output]
    words = [i[4] for i in words3]
    r = [input_words + i for i in words]
    print('3-gram联想结果为：', r)
    return r


if __name__ == '__main__':
    # 语料路径
    file_path = r'E:\5.工作\2024禾唱\输入法\语料\和合本圣经经文词库2.csv'
    review = dataLoad(file_path)

    # 将语料中的每个字拆分成单个字
    singleReView = [' '.join(list(r)) for r in review]

    # 根据语料创建2-gram词袋
    cv2 = CountVectorizer(ngram_range=(2, 2), analyzer='word', token_pattern=r'\w')
    cv2_fit = cv2.fit_transform(singleReView)
    # 所有两个字的组合，以及他们在词袋中的索引
    gram2voc = cv2.vocabulary_
    # 所有两个字组合在语料库中出现的频数
    temp2 = cv2_fit.sum(axis=0)
    freqList2 = sum(temp2.getA().tolist(), [])

    # 根据语料创建n-gram3的词袋
    cv3 = CountVectorizer(ngram_range=(3, 3), analyzer='word', token_pattern=r'\w')
    cv3_fit = cv3.fit_transform(singleReView)
    # 所有两个字的组合，以及他们在词袋中的索引
    gram3voc = cv3.vocabulary_
    # 所有两个字的组合在语料库中出现的频数
    temp3 = cv3_fit.sum(axis=0)
    freqList3 = sum(temp3.getA().tolist(), [])

    while True:
        s = input('请输入要联想的单词或词组：')
        if s == 'exit':
            break
        print('输入的字数：', len(s))
        num = input('请输入要联想的单词或词组的数量：')
        # 尝试将 num 转换为整数
        try:
            num = int(num)
        except ValueError:
            print('请输入一个有效的整数！')
            continue
        if len(s) == 1:
            print('输入的字数等于1，将使用2-gram进行联想。')
            result = gram2(gram2voc, s, freqList2, num)
        elif len(s) > 1:
            print('输入的字数大于1，将使用3-gram进行联想。')
            result = gram3(gram3voc, s, freqList3, num)
        else:
            print('输入不能为空！')
