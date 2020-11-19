import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;

/**
 用于结果保存的工具类
 @author qian
 */
@Slf4j
public class CSVTools {
    /**
     * 将向量（一行数据）保存到csv文件中
     * @param outputDir 输出目录
     * @param type 输出类型
     * @param fileName 保存文件名（不含.csv扩展名）
     * @param features 特征：一层List
     */
    public static <T> void saveVector(String outputDir, String type, String fileName, List<T> features) {
        Path path = Paths.get(outputDir, type, fileName + ".csv");
        try {
            Files.write(path,
                    features.stream()
                            .map(T::toString)
                            .collect(Collectors.joining(","))
                            .getBytes(),
                    StandardOpenOption.CREATE);
        } catch (IOException e) {
            log.error(String.join(" ", "Vector IOException:", type, fileName));
        }
    }

    /**
     * 将矩阵（多行数据）保存到csv文件中
     * @param outputDir 输出目录
     * @param type 输出类型
     * @param fileName 保存文件名（不含.csv扩展名）
     * @param features 特征：两层List
     */
    public static <T> void saveMatrix(String outputDir, String type, String fileName, List<List<T>> features) {
        Path path = Paths.get(outputDir, type, fileName + ".csv");
        try {
            Files.write(path,
                    features.stream()
                            .map(line -> line.stream()
                                        .map(T::toString)
                                        .collect(Collectors.joining(","))
                            )
                            .collect(Collectors.joining("/n"))
                            .getBytes(),
                    StandardOpenOption.CREATE);
        } catch (IOException e) {
            log.error(String.join(" ", "Vector IOException:", type, fileName));
        }
    }

    /**
     * 创建输出目录下保存结果的子文件夹
     * @param outputDir 输出目录
     * @param types 输出类型数组
     */
    public static void createOutputDir(String outputDir, String... types) {
        for (String type : types) {
            try {
                Files.createDirectories(Paths.get(outputDir, type));
            } catch (FileAlreadyExistsException e1) {
                log.error(type + " Directory Already Exists: " + e1.getMessage());
            } catch (IOException e2) {
                log.error(e2.getMessage());
            }
        }
    }
}
