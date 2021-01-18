import com.github.javaparser.Position;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.stmt.CatchClause;
import lombok.extern.slf4j.Slf4j;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

@Slf4j
public class SliceHandler {
    /**
     * 根据给出的行号对目录下的Java文件进行切片操作
     * 目前暂未考虑子目录的情况
     * 输出格式：文件名#切片行.csv
     * @param inputDir 输入文件目录
     * @param outputDir 输出文件目录
     * @param lineFile 保存切片行号的csv文件地址
     */
    public static void sliceByLines(String inputDir, String outputDir, String lineFile) {
        // 读取保存切片行号的csv文件
        try (BufferedReader reader = new BufferedReader(new FileReader(lineFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] lineData = line.split(",");
                // 每行第一个数据为文件名
                Path javaFilePath = Paths.get(inputDir, lineData[0] + ".java");
                // 后续数据为切片行号
                List<Integer> sliceLines = new ArrayList<>();
                for (int i = 1; i < lineData.length; i++) {
                    sliceLines.add(Integer.parseInt(lineData[i]));
                }
                Path sliceFilePath = Paths.get(outputDir, lineData[0] + "#" + lineData[lineData.length - 1] + ".java");

                if (!Files.exists(sliceFilePath)) {
                    Files.createFile(sliceFilePath);
                }
                try (BufferedWriter writer = new BufferedWriter(new FileWriter(sliceFilePath.toFile()))) {
                    writer.write(sliceFile(javaFilePath.toFile(), sliceLines));
                    log.info(sliceFilePath.toString());
                } catch (IOException e) {
                    log.error(e.toString() + " " + lineFile);
                }

            }
        } catch (IOException e) {
            log.error(e.toString() + " " + lineFile);
        }


    }

    /**
     * 对指定的方法体进行切片操作，保留与切片行号有关的代码
     * @param file Java文件对象
     * @param methodName 需要切片的方法名
     * @param lines 切片行号列表
     * @return 处理完成的Java文件内容
     */
    private static String sliceFile(File file, String methodName, List<Integer> lines) {
        try {
            CompilationUnit cu = StaticJavaParser.parse(file);
            List<MethodDeclaration> methodList = cu.findAll(MethodDeclaration.class);
            for (MethodDeclaration m : methodList) {
                if (methodName.equals(m.getNameAsString())) {
                    // 方法体存在
                    if (m.getBody().isPresent()) {
                        m.getBody().get().walk(node -> {
                            sliceMethod(node, lines);
                        });
                        return cu.toString();
                    }
                } else {
                    m.remove();
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            log.error(e.toString() + " " + file.getAbsolutePath());
        }
        log.error(String.format("%s method not in %s", methodName, file.getAbsolutePath()));
        return "";
    }

    private static String sliceFile(File file, List<Integer> lines) {
        try {
            CompilationUnit cu = StaticJavaParser.parse(file);
            List<MethodDeclaration> methodList = cu.findAll(MethodDeclaration.class);
            for (MethodDeclaration m : methodList) {
                m.getRange().ifPresent(r -> {
                    if (r.contains(new Position(lines.get(0), 100))) {
                        sliceMethod(m, lines);
                    }
                });
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            log.error(e.toString() + " " + file.getAbsolutePath());
        }
        return "";
    }

    private static void sliceMethod(Node method, List<Integer> lines) {
        // 到根节点的路径上如果有CatchClause节点，直接保留此节点
        // 目前没有考虑try-catch的嵌套
        Node p = method;
        while (true) {
            if (p.getParentNode().isPresent()) {
                if (p instanceof CatchClause) {
                    return;
                }
                p = p.getParentNode().get();
            } else {
                break;
            }
        }
        // 检查节点对应的行号范围
        if (method.getRange().isPresent()) {
            int startLine = method.getRange().get().begin.line;
            int endLine = method.getRange().get().end.line;
            // 切片行号中是否存在一行在节点的代码范围内
            boolean contained = false;
            for (int line : lines) {
                if (startLine <= line && line <= endLine) {
                    contained = true;
                    break;
                }
            }
            // 不存在说明节点中不包含需要保留到切片的代码，故删除
            if (!contained) {
                method.remove();
            }
        }
    }
}
