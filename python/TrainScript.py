import os
import re
import sys
import pandas as pd
from DataSet import DataLoader
from TrainTask import VectorTask, ManualTask, WordTask


def result_lines(feature: str, to_vector: str, result_dict: dict):
    """
    结果转换为csv中的行记录
    """
    lines = []
    for model_name, result in result_dict.items():
        lines.append({
            "feature": feature,
            "to_vector": to_vector,
            "model_name": model_name,
            "acc": result[0],
            "pre": result[1],
            "rec": result[2],
            "f1": result[3],
            "auc": result[4],
        })
    return lines


def train_once(feature_root, label_file, output_path, run_time):
    df = pd.DataFrame(columns=["feature", "to_vector", "model_name", "acc", "pre", "rec", "f1", "auc"])
    for feature_dir in os.listdir(feature_root):
        if os.path.isdir(os.path.join(feature_root, feature_dir)):
            name_list = feature_dir.split("_")
            if "v" in feature_dir:
                t = VectorTask(os.path.join(feature_root, feature_dir), label_file, int(name_list[-1]))
                t.run(run_time, 0.7)
                feature_name = re.findall(r"(.*?)_v", feature_dir)[0]
                vector_method = re.search(r"v_(.*)", feature_dir).group()
                df = df.append(result_lines(feature_name, vector_method, t.get_result()), ignore_index=True)
            elif "manual" in feature_dir:
                t = ManualTask(os.path.join(feature_root, feature_dir), label_file)
                t.run(run_time, 0.7)
                df = df.append(result_lines("manual", "", t.get_result()), ignore_index=True)
            else:
                t = WordTask(os.path.join(feature_root, feature_dir), label_file, "Count")
                t.run(run_time, 0.7)
                df = df.append(result_lines(feature_dir, "Count", t.get_result()), ignore_index=True)
                t = WordTask(os.path.join(feature_root, feature_dir), label_file, "OneHot")
                t.run(run_time, 0.7)
                df = df.append(result_lines(feature_dir, "OneHot", t.get_result()), ignore_index=True)

    df.to_csv(output_path, header=True, index_label=False)


if __name__ == "__main__":
    feature_root = sys.argv[1]
    label_file = sys.argv[2]
    output_path = sys.argv[3]
    run_time = int(sys.argv[4])
    sample_method = sys.argv[5] if len(sys.argv) > 5 else "All"
    if sample_method == "Over":
        DataLoader.over_sample = True
    if sample_method == "Under":
        DataLoader.under_sample = True
    if sample_method == "All":
        train_once(feature_root, label_file, output_path, run_time)
    if sample_method == "Category":
        category_list = ["cmdi", "crypto", "hash", "sqli", "pathtraver", "weakrand", "securecookie", "trustbound",
                         "xpathi", "xss", "ldapi"]
        for c in category_list:
            try:
                DataLoader.category_list = [c]
                train_once(feature_root, label_file, os.path.join(output_path, c + ".csv"), run_time)
            except:
                continue
    if sample_method == "Study":
        DataLoader.category_list = ["cmdi", "sqli", "xpathi", "xss", "ldapi"]
        train_once(feature_root, label_file, output_path, run_time)
