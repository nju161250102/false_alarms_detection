import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;

public class MainApp {

    // 数据目录
    private static final String dataRootDir = "/home/qmy/Data";
    // 源代码文件夹
    private static final String sourceCodeDir = "OwaspMethod";
    // 格式化修改之后的源代码文件夹
    private static final String modifyCodeDir = "ModifiedMethod";
    // 切片代码文件夹
    private static final String sliceCodeDir = "OwaspSlice";
    // 提取特征文件夹
    private static final String featureDir = "MethodFeature";
    // 提取切片特征文件夹
    private static final String sliceFeatureDir = "SliceFeature";
    // 切片行标签
    private static final String sliceLineFile = "slice.csv";

    public static void main(String[] args) {
        List<String> arguments = Arrays.asList(args);
        // 格式化输出源代码
        if (arguments.contains("format")) {
            FileHandler.prettyPrint(joinPath(sourceCodeDir), joinPath(modifyCodeDir));
        }
        // 切片操作
        if (arguments.contains("slice")) {
            SliceHandler.sliceByLines(joinPath(modifyCodeDir), joinPath(sliceCodeDir), joinPath(sliceLineFile));
        }
        // 特征提取
        if (arguments.contains("extract")) {
            FeatureHandler.extractFiles(joinPath(modifyCodeDir), joinPath(featureDir));
        }
        // 对切片的特征提取
        if (arguments.contains("extract_slice")) {
            FeatureHandler.extractFiles(joinPath(sliceCodeDir), joinPath(sliceFeatureDir));
        }
    }

    private static String joinPath(String... strings) {
        return Paths.get(dataRootDir, strings).toString();
    }

}
