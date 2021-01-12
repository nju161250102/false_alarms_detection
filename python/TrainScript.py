import os
import sys
import logging
import tensorflow as tf
from dataset import DataLoader
from task import TaskFactory
from .Config import Config

# ------设置------
tf.get_logger().setLevel('ERROR')
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s\t  %(levelname)s\t  %(message)s",
                    datefmt="%Y-%M-%d %H:%M:%S")


if __name__ == "__main__":
    method_task = TaskFactory(Config.method_feature, Config.original_label)
    method_task.add_tasks(list(filter(lambda s: s == "word" or "v" in s, os.listdir(Config.method_feature))))
    method_task.run_and_save(os.path.join(Config.output_dir, "featureTask0110.csv"), Config.run_time)
