import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.visitor.VoidVisitor;
import lombok.extern.slf4j.Slf4j;
import preprocess.SeqVisitor;
import preprocess.SymbolTools;
import word2vec.Word2VecModel;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

@Slf4j
public class FeatureHandler {
    public static void extractFiles(String inputDir, String outputDir) {
        Map<String, String> documents = new HashMap<>();
        CSVTools.createOutputDir(outputDir, "word", "ast", "wordV", "astV", "docV", "type");
        try {
            Files.walk(Paths.get(inputDir))
                    .filter(path -> "java".equals(path.toString().substring(path.toString().lastIndexOf(".") + 1)))
                    .forEach(path -> {
                        File javaFile = path.toFile();
                        log.info(path.toString());
                        try {
                            CompilationUnit cu = StaticJavaParser.parse(javaFile);
                            List<MethodDeclaration> methodList = cu.findAll(MethodDeclaration.class);
                            for (MethodDeclaration m : methodList) {
                                if (m.isConstructorDeclaration()) continue;
                                if (! m.getNameAsString().equals("doPost")) continue;
                                m.getAllContainedComments().forEach(Comment::remove);
                                SymbolTools.nameSubstitute(m);

                                List<String> words = extractWord(m);
                                List<String> astWords = extractASTWord(m);
                                List<String> typeWords = extractNodeType(m);
                                documents.put(javaFile.getName(), String.join(" ", words));

                                String outputName = javaFile.getName().split("\\.")[0] + "#" + m.getNameAsString();

                                CSVTools.saveVector(outputDir, "word", outputName, words);
                                CSVTools.saveVector(outputDir, "ast", outputName, astWords);
                                CSVTools.saveVector(outputDir, "type", outputName, typeWords);
                                CSVTools.saveMatrix(outputDir, "wordV", outputName, Word2VecModel.transformWords(words, 16));
                                CSVTools.saveMatrix(outputDir, "astV", outputName, Word2VecModel.transformWords(astWords, 16));
                            }
                        } catch (FileNotFoundException e1) {
                            e1.printStackTrace();
                            log.error(e1.toString() + " " + path.toString());
                        }
                    });
        } catch (IOException e) {
            e.printStackTrace();
        }
        Map<String, List<Double>> result = Word2VecModel.transformParagraph(documents, 16);
        result.forEach((javaFileName, data) -> {
            CSVTools.saveVector(outputDir, "docV", javaFileName.split("\\.")[0], data);
        });
    }

    public static void extractSliceFile(String inputDir, String outputDir) {
        try {
            Map<String, String> documents = new HashMap<>();
            Files.list(Paths.get(inputDir)).forEach(f -> {
                try {
                    List<String> lines = Files.readAllLines(f);
                    log.info(f.toString());
                    lines.remove(0);
                    lines.remove(0);
                    documents.put(f.getFileName().toString(), String.join(" ", lines));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
            Map<String, List<Double>> result = Word2VecModel.transformParagraph(documents, 32);
            CSVTools.createOutputDir(outputDir, "byte");
            result.forEach((fileName, data) -> {
                CSVTools.saveVector(outputDir, "byte", fileName.substring(0, 18), data);
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static List<String> extractWord(MethodDeclaration method) {
        StringTokenizer stringTokenizer = new StringTokenizer(method.toString(), " \t\n\r\f\";+-.*/(){},=?:");
        List<String> words = new ArrayList<>();
        while (stringTokenizer.hasMoreElements()) {
            words.add(stringTokenizer.nextToken());
        }
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
}
