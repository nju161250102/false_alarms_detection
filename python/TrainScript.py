import os
import sys
from dataset import DataLoader
from task import TaskFactory

# ------设置------
method_feature = "/home/qmy/Data/MethodFeature/"
slice_feature = "/home/qmy/Data/SliceFeature/"
original_label = "/home/qmy/Data/label.csv"
slice_label = "/home/qmy/Data/slice_label1.csv"
slice_handle_label = "/home/qmy/Data/slice_label2.csv"
output_dir = "/home/qmy/Data/"
category_dir = "/home/qmy/Data/CategoryResult/"
run_time = 10
category_list = ["cmdi", "crypto", "hash", "sqli", "pathtraver", "weakrand", "securecookie", "trustbound",
                         "xpathi", "xss", "ldapi"]
study_list = ["cmdi", "sqli", "xpathi", "xss", "ldapi"]


if __name__ == "__main__":
    method_task = TaskFactory(method_feature, original_label)
    method_task.add_tasks(list(filter(lambda s: s == "word" or "v" in s, os.listdir(method_feature))))
    method_task.run_and_save(os.path.join(output_dir, "featureTask0109.csv"), run_time)
