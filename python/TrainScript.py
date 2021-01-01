import os
import sys
import pandas as pd
from DataSet import DataLoader
from TrainTask import VectorTask, ManualTask, WordTask


def result_lines(data_set: str, feature_extraction: str, result_dict: dict):
    """
    结果转换为csv中的行记录
    """
    lines = []
    for model_name, result in result_dict.items():
        lines.append({
            "data_set": data_set,
            "feature_extraction": feature_extraction,
            "model_name": model_name,
            "acc": result[0],
            "pre": result[1],
            "rec": result[2],
            "f1": result[3],
            "auc": result[4],
        })
    return lines


if __name__ == "__main__":
    feature_root = sys.argv[1]
    label_file = sys.argv[2]
    output_path = sys.argv[3]
    run_time = int(sys.argv[4])
    sample_method = sys.argv[5]
    if sample_method == "Over":
        DataLoader.over_sample = True
    if sample_method == "Under":
        DataLoader.under_sample = True
    df = pd.DataFrame(columns=["data_set", "feature_extraction", "model_name", "acc", "pre", "rec", "f1", "auc"])
    for feature_dir in os.listdir(feature_root):
        if os.path.isdir(os.path.join(feature_root, feature_dir)):
            name_list = feature_dir.split("_")
            if "v" in feature_dir:
                t = VectorTask(os.path.join(feature_root, feature_dir), label_file, int(name_list[-1]))
                t.run(run_time, 0.7)
                df = df.append(result_lines("word", feature_dir, t.get_result()), ignore_index=True)
            elif "manual" in feature_dir:
                t = ManualTask(os.path.join(feature_root, feature_dir), label_file)
                t.run(run_time, 0.7)
                df = df.append(result_lines("manual", "", t.get_result()), ignore_index=True)
            else:
                t = WordTask(os.path.join(feature_root, feature_dir), label_file, "Count")
                t.run(run_time, 0.7)
                df = df.append(result_lines(feature_dir, "Count", t.get_result()), ignore_index=True)
                t = WordTask(os.path.join(feature_root, feature_dir), label_file, "Tf")
                t.run(run_time, 0.7)
                df = df.append(result_lines(feature_dir, "Tf", t.get_result()), ignore_index=True)
            print()
    df.to_csv(output_path, header=True, index_label=False)
