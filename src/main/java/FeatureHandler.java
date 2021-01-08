import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.visitor.VoidVisitor;
import lombok.extern.slf4j.Slf4j;
import preprocess.SeqVisitor;
import preprocess.SymbolTools;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@Slf4j
public class FeatureHandler {
    /**
     * 提取指定文件夹下的Java代码特征
     * @param inputDir 代码输入文件夹
     * @param outputDir 特征输出文件夹
     */
    public static void extractFiles(String inputDir, String outputDir) {
        // 创建输出目录
        CSVTools.createOutputDir(outputDir, "word_ans", "ast", "word_aps", "word_ext", "type");
        try {
            Files.walk(Paths.get(inputDir))
                    .filter(path -> "java".equals(path.toString().substring(path.toString().lastIndexOf(".") + 1)))
                    .forEach(path -> extractSingleFile(path.toFile(), outputDir));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 对单个java文件的特征提取操作
     * @param javaFile File文件对象
     */
    public static void extractSingleFile(File javaFile, String outputDir) {
        log.info(javaFile.getPath());
        try {
            // 解析Java文件
            CompilationUnit cu = StaticJavaParser.parse(javaFile);
            for (MethodDeclaration m : cu.findAll(MethodDeclaration.class)) {
                // 指定处理doPost方法
                if (m.getNameAsString().equals("doPost")) {
                    // 预处理：清除注释，变量名替换
                    m.getAllContainedComments().forEach(Comment::remove);
                    SymbolTools.nameSubstitute(m);
                    // 特征提取与保存
                    String outputName = javaFile.getName().split("\\.")[0] + "#" + m.getNameAsString();
                    CSVTools.saveVector(outputDir, "word", outputName, extractWord(m));
                    CSVTools.saveVector(outputDir, "word_ans", outputName, extractWord(m, false, false));
                    CSVTools.saveVector(outputDir, "word_aps", outputName, extractWord(m, false, true));
                    CSVTools.saveVector(outputDir, "word_ext", outputName, extractWord(m, true, true));
                    CSVTools.saveVector(outputDir, "ast", outputName, extractASTWord(m));
                    CSVTools.saveVector(outputDir, "type", outputName, extractNodeType(m));
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            log.error(e.toString());
        }
    }

    /**
     * 根据方法体进行简单的分词
     * @param method 方法体
     * @return word序列
     */
    public static List<String> extractWord(MethodDeclaration method) {
        List<String> words = new ArrayList<>();
        StringTokenizer stringTokenizer = new StringTokenizer(method.toString(), " \t\n\r\f\";+-.*/(){}[],=!?:");
        while (stringTokenizer.hasMoreElements()) {
            words.add(stringTokenizer.nextToken());
        }
        return words;
    }

    /**
     * 从方法体中提取word序列
     * @param method 方法体
     * @param wordSplit 是否需要对单词进行分割
     * @param unknownMark 是否需要将低频变量设为UNK
     * @return word序列
     */
    public static List<String> extractWord(MethodDeclaration method, boolean wordSplit, boolean unknownMark) {
        // 分词
        List<String> words = new ArrayList<>();
        StringTokenizer stringTokenizer = new StringTokenizer(method.toString(), " \t\n\r\f\";+-.*/(){}[],=!?:");
        while (stringTokenizer.hasMoreElements()) {
            if (wordSplit) {
                words.addAll(Arrays.asList(splitName(stringTokenizer.nextToken())));
            } else {
                words.add(stringTokenizer.nextToken());
            }
        }
        // 对变量出现次数计数
        Map<String, Long> varCountMap = words.stream()
                .filter(s -> s.startsWith("VAR"))
                .collect(Collectors.groupingBy(s -> s, Collectors.counting()));
        words = words.stream()
                .map(s -> {
                    // 替换数字
                    if (Pattern.matches("[0-9]+", s)) {
                        if (Math.abs(Integer.parseInt(s)) < 10) {
                            return s;
                        } else {
                            return "N" + s.length();
                        }
                    }
                    // 替换为UNK
                    else if (unknownMark && s.startsWith("VAR") && varCountMap.get(s) <= 1) {
                        return "UNK";
                    } else {
                        return s;
                    }
                })
                .collect(Collectors.toList());
        return words;
    }

    private static List<String> extractASTWord(MethodDeclaration method) {
        List<String> astWords = new ArrayList<>();
        VoidVisitor<List<String>> voidVisitor = new SeqVisitor();
        voidVisitor.visit(method, astWords);
        return astWords;
    }

    private static List<String> extractNodeType(MethodDeclaration method) {
        List<String> result = new ArrayList<>();
        method.getBody().ifPresent(body -> {
            body.walk(node -> {
                String typeName = node.getClass().getName();
                result.add(typeName.substring(typeName.lastIndexOf(".") + 1));
            });
        });
        return result;
    }

    /**
     * 切分驼峰命名单词
     * @param name 变量名
     * @return 拆分单词结果
     */
    private static String[] splitName (String name) {
        String result = "";
        if (name != null) {
            // 判断是否是下划线命名
            if (! Pattern.matches(".*[_]+.*", name)) {
                // 判断是否包含大写字母
                if (! Pattern.matches(".*[A-Z]+.*", name)) {
                    return new String[]{name};
                }
                result = name.replaceAll( "([a-z])([A-Z])", "$1" + "_" + "$2" );
            }
            return result.split("_");
        }
        return new String[]{};
    }
}
