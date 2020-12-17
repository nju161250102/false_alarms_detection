package preprocess;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.body.MethodDeclaration;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.FileNotFoundException;

import static org.junit.jupiter.api.Assertions.*;

class SymbolToolsTest {
    @Test
    void nameSubstitute() {
        try {
            CompilationUnit cu = StaticJavaParser.parse(new File("/home/qian/Documents/Work/Data/ModifiedMethod/BenchmarkTest00001.java"));
            for (MethodDeclaration m : cu.findAll(MethodDeclaration.class)) {
                if (m.isConstructorDeclaration()) continue;
                SymbolTools.nameSubstitute(m);
                System.out.println(m);
            }
        } catch (FileNotFoundException e1) {
            e1.printStackTrace();
        }
    }
}