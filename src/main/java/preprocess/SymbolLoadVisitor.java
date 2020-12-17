package preprocess;

import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.StringLiteralExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.Map;

/**
 * 遍历AST树得到变量/字符串的类型映射
 */
public class SymbolLoadVisitor extends VoidVisitorAdapter<Map<String, String>> {

    // 记录声明的变量
    public void visit(VariableDeclarator declarator, Map<String, String> typeMap) {
        if (! typeMap.containsKey(declarator.getNameAsString()))
            typeMap.put(declarator.getNameAsString(), "VAR");
        super.visit(declarator, typeMap);
    }

    // 记录参数中的变量
    public void visit(Parameter parameter, Map<String, String> typeMap) {
        if (! typeMap.containsKey(parameter.getNameAsString()))
            typeMap.put(parameter.getNameAsString(), "VAR");
        super.visit(parameter, typeMap);
    }

    // 记录字符串
    public void visit(StringLiteralExpr expr, Map<String, String> typeMap) {
        if (! typeMap.containsKey(expr.asString()))
            typeMap.put(expr.asString(), "STR");
        super.visit(expr, typeMap);
    }

}
