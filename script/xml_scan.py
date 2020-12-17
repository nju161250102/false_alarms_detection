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
                    line = []
                    line.append(os.path.splitext(f)[0])
                    line.append(item.get("category"))
                    line.append(item.get("type"))
                    line.append(item.find("Method").get("name"))
                    line.append(item.find("Class").get("classname"))
                    line.append("" if item.find("SourceLine") is None else item.find("SourceLine").get("start"))
                    data.append(line)
        except:
            continue
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(sys.argv[2], "result.csv"), header=False, index_label=False)

