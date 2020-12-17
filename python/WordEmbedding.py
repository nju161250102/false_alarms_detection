import os
import sys
import numpy as np
from alive_progress import alive_bar
from gensim.models import word2vec


def get_word_vector(file_path, feature_size):
    with open(file_path, "r") as f:
        sentences = f.readline().split(",")
        model = word2vec.Word2Vec([sentences], sg=1, size=feature_size,  window=5,  min_count=1, sample=0.001, workers=4)
        return np.array([model.wv[word] for word in sentences])


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    feature_size = int(sys.argv[3])
    file_list = os.listdir(input_dir)
    with alive_bar(len(file_list)) as bar:
        for f in file_list:
            vector_matrix = get_word_vector(os.path.join(input_dir, f), feature_size)
            np.savetxt(os.path.join(output_dir, f), vector_matrix, delimiter=",")
            bar()
