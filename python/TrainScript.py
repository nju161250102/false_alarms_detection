import os
import sys
import pandas as pd
from TrainTask import *


def result_lines(data_set: str, feature_extraction: str, result_dict: dict):
    result = []
    for model_name, result in result_dict:
        result.append({
            "data_set": data_set,
            "feature_extraction": feature_extraction,
            "model_name": model_name,
            "acc": result[0],
            "pre": result[1],
            "rec": result[2],
            "f1": result[3],
            "auc": result[4],
        })
    return result


if __name__ == "__main__":
    feature_root = sys.argv[1]
    label_file = sys.argv[2]
    output_path = sys.argv[3]
    run_time = int(sys.argv[4])
    df = pd.DataFrame(columns=["data_set", "feature_extraction", "model_name", "acc", "pre", "rec", "f1", "auc"])
    for feature_dir in os.listdir(feature_root):
        if os.path.isdir(feature_dir):
            name_list = feature_dir.split("_")
            if "v" in feature_dir:
                t = VectorTask(os.path.join(feature_root, feature_dir), label_file, int(name_list[-1]))
                t.run(run_time, 0.7)
                df = df.append(result_lines("word", feature_dir, t.result_data), ignore_index=True)
            elif "manual" in feature_dir:
                t = ManualTask(os.path.join(feature_root, feature_dir), label_file)
                t.run(run_time, 0.7)
                df = df.append(result_lines("manual", "", t.result_data), ignore_index=True)
            else:
                t = WordTask(os.path.join(feature_root, feature_dir), label_file, "Count")
                t.run(run_time, 0.7)
                df = df.append(result_lines(feature_dir, "Count", t.result_data), ignore_index=True)
                t = WordTask(os.path.join(feature_root, feature_dir), label_file, "Tf")
                t.run(run_time, 0.7)
                df = df.append(result_lines(feature_dir, "Tf", t.result_data), ignore_index=True)
    df.to_csv(output_path, header=True, index_label=False)
