from xml.etree.ElementTree import parse
import os
import sys
import pandas as pd


if __name__ == "__main__":
    data = []
    for f in os.listdir(sys.argv[1]):
        try:
            if os.path.splitext(f)[-1] == ".xml":
                doc = parse(os.path.join(sys.argv[1], f))
                for item in doc.iterfind("BugInstance"):
                    if item.find("SourceLine") is not None:
                        line = []
                        line.append(os.path.splitext(f)[0].split("_")[0])
                        line.append(os.path.splitext(f)[0].split("_")[1])
                        line.append(item.get("category"))
                        line.append(item.get("type"))
                        line.append(item.get("rank"))
                        class_name = item.find("Class").get("classname")
                        line.append(class_name)
                        for method_node in item.findall("Method"):
                            if method_node.get("classname") == class_name:
                                line.append(method_node.get("name"))
                                start_line = int(method_node.find("SourceLine").get("start"))
                                end_line = int(method_node.find("SourceLine").get("end"))
                        if len(line) != 7:
                            continue
                        line.append(0)
                        for source_line in item.findall("SourceLine"):
                            if start_line <= int(source_line.get("start")) <= end_line:
                                line[-1] = int(source_line.get("start"))
                                data.append(line[:])
        except Exception as e:
            print(f, e)
            continue
    df = pd.DataFrame(data, columns=["Project", "BugId", "Category", "Type", "Rank", "Class", "Method", "Line"])
    df.to_csv(os.path.join(sys.argv[2], "result.csv"), header=True, index=False)

