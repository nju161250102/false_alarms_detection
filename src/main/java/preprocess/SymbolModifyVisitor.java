package preprocess;

import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.TryStmt;
import com.github.javaparser.ast.visitor.ModifierVisitor;

import java.util.Map;

/**
 * 借助Map中的变量名替换映射修改AST树
 */
public class SymbolModifyVisitor extends ModifierVisitor<Map<String, String>> {

    // 修改变量声明时的变量名
    public VariableDeclarator visit(VariableDeclarator declarator, Map<String, String> map) {
        if (map.containsKey(declarator.getNameAsString()))
            declarator.setName(map.get(declarator.getNameAsString()));
        super.visit(declarator, map);
        return declarator;
    }

    // 只保留Try-Catch语句的TryBlock部分
    public BlockStmt visit(TryStmt stmt, Map<String, String> map) {
        super.visit(stmt, map);
        return stmt.getTryBlock();
    }

    // 修改方法参数名
    public Parameter visit(Parameter parameter, Map<String, String> map) {
        if (map.containsKey(parameter.getNameAsString()))
            parameter.setName(map.get(parameter.getNameAsString()));
        super.visit(parameter, map);
        return parameter;
    }

    // 修改变量名
    public SimpleName visit(SimpleName name, Map<String, String> map) {
        if (map.containsKey(name.asString()))
            name.setIdentifier(map.get(name.asString()));
        super.visit(name, map);
        return name;
    }

    // 修改字符串
    public StringLiteralExpr visit(StringLiteralExpr expr, Map<String, String> map) {
        if (map.containsKey(expr.asString()))
            expr.setString(map.get(expr.asString()));
        super.visit(expr, map);
        return expr;
    }

}
