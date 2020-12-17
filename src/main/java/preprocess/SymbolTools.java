package preprocess;

import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.visitor.ModifierVisitor;

import java.util.HashMap;
import java.util.Map;

public class SymbolTools {

    public static void nameSubstitute(MethodDeclaration declaration) {
        // 去除方法注解
        declaration.setAnnotations(new NodeList<>());
        Map<String, String> typeMap = new HashMap<>();
        SymbolLoadVisitor loadVisitor = new SymbolLoadVisitor();
        loadVisitor.visit(declaration, typeMap);
        ModifierVisitor<Map<String, String>> modifyVisitor = new SymbolModifyVisitor();
        modifyVisitor.visit(declaration, getNameMap(typeMap));
    }

    /**
     * 从变量名到变量类型的映射获取变量名替换的映射
     * @param typeMap Map<变量名, 变量类型VAR/STR>
     * @return Map<旧变量名, 新变量名>
     */
    private static Map<String, String> getNameMap(Map<String, String> typeMap) {
        Map<String, Integer> countMap = new HashMap<>();
        Map<String, String> resultMap = new HashMap<>();
        for (String key : typeMap.keySet()) {
            countMap.merge(typeMap.get(key), 1, Integer::sum);
            resultMap.put(key, typeMap.get(key) + countMap.get(typeMap.get(key)));
        }
        return resultMap;
    }
}
