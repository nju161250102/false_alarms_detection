import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import org.junit.Test;
import preprocess.SymbolTools;

import java.io.File;
import java.io.FileNotFoundException;

public class FeatureHandlerTest {
    @Test
    public void extractFiles() {
//        String inputDir = "/home/qian/Documents/Work/Data/OwaspMethod";
//        String outputDir = "/home/qian/Documents/Work/Data/MethodFeature";
        String sliceInputDir = "/home/qian/Documents/Work/Data/OwaspSlice2/";
        String sliceOutputDir = "/home/qian/Documents/Work/Data/SliceFeature/";
//        FeatureHandler.extractFiles(inputDir, outputDir);
        FeatureHandler.extractFiles(sliceInputDir, sliceOutputDir);
    }

    @Test
    public void extractWord() {
        try {
            CompilationUnit cu = StaticJavaParser.parse(new File("/home/qian/Documents/Work/Data/ModifiedMethod/BenchmarkTest00001.java"));
            for (MethodDeclaration m : cu.findAll(MethodDeclaration.class)) {
                if ("doPost".equals(m.getNameAsString())) {
                    SymbolTools.nameSubstitute(m);
                    System.out.println(FeatureHandler.extractWord(m, true, true));
                }
            }
        } catch (FileNotFoundException e1) {
            e1.printStackTrace();
        }
    }

    @Test
    public void extractBytes() {
        String inputDir = "/home/qian/Documents/Work/mangrove/data/slices/owasp";
        String outputDir = "/home/qian/Documents/Work/Data/SliceFeature";
        FeatureHandler.extractSliceFile(inputDir, outputDir);
    }
}