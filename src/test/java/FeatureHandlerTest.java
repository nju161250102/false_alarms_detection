import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import org.junit.Test;
import preprocess.SymbolTools;

import java.io.File;
import java.io.FileNotFoundException;

public class FeatureHandlerTest {

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

}