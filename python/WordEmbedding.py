import os
import sys
import numpy as np
from alive_progress import alive_bar
from gensim.models import word2vec

"""
使用word2vec模型生成文本序列的特征向量表示
args: 输入目录 输出目录 特征大小
"""
if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    feature_size = int(sys.argv[3])
    file_list = os.listdir(input_dir)
    with alive_bar(len(file_list)) as bar:
        for file in file_list:
            with open(os.path.join(input_dir, file), "r") as f:
                sentences = f.readline().split(",")
                model = word2vec.Word2Vec([sentences], sg=1, size=feature_size, window=5, min_count=1, sample=0.001,
                                          workers=4)
                np.savetxt(os.path.join(output_dir, file), [model.wv[word] for word in sentences], delimiter=",")
            bar()
