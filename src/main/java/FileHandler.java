import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.printer.PrettyPrinter;
import com.github.javaparser.printer.PrettyPrinterConfiguration;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

@Slf4j
public class FileHandler {
    /**
     * 调整目录下Java文件的格式
     * @param inputDir 存放Java文件的目录
     * @param outputDir 保存格式统一的Java文件的目录
     */
    public static void prettyPrint(String inputDir, String outputDir) {
        try {
            Files.walk(Paths.get(inputDir))
                    .filter(path -> "java".equals(path.toString().substring(path.toString().lastIndexOf(".") + 1)))
                    .forEach(path -> {
                        try {
                            CompilationUnit cu = StaticJavaParser.parse(path.toFile());
                            PrettyPrinterConfiguration conf = new PrettyPrinterConfiguration();
                            conf.setIndentSize(4);
                            conf.setPrintComments(false);
                            PrettyPrinter prettyPrinter = new PrettyPrinter(conf);
                            Files.write(Paths.get(outputDir, path.getFileName().toString()), prettyPrinter.print(cu).getBytes());
                            log.info("Print " + path.getFileName());
                        } catch (IOException e) {
                            log.error(e.toString() + " " + path);
                        }
                    });
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
