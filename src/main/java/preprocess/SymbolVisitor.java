package preprocess;

import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.BinaryExpr;
import com.github.javaparser.ast.expr.IntegerLiteralExpr;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.expr.StringLiteralExpr;
import com.github.javaparser.ast.visitor.ModifierVisitor;

import java.util.HashMap;
import java.util.Map;

public class SymbolVisitor extends ModifierVisitor<Void> {

    private Map<String, Integer> numberMap = new HashMap<>();
    private Map<String, String> nameMap = new HashMap<>();

    public VariableDeclarator visit(VariableDeclarator declarator, Void arg) {
        putSymbol(declarator.getTypeAsString(), declarator.getNameAsString());
        super.visit(declarator, arg);
        return declarator;
    }

    public Parameter visit(Parameter parameter, Void arg) {
        putSymbol(parameter.getTypeAsString(), parameter.getNameAsString());
        super.visit(parameter, arg);
        return parameter;
    }

    public SimpleName visit(SimpleName name, Void arg) {
        if (nameMap.containsKey(name.asString())) {
            name.setIdentifier(nameMap.get(name.asString()));
        }
        super.visit(name, arg);
        return name;
    }

    public StringLiteralExpr visit(StringLiteralExpr expr, Void arg) {
        if (nameMap.containsKey(expr.asString())) {
            expr.setString(nameMap.get(expr.asString()));
        } else {
            putSymbol("STRING_EXPR", expr.asString());
        }
        super.visit(expr, arg);
        return expr;
    }

    public StringLiteralExpr visit(BinaryExpr expr, Void arg) {
        putSymbol("BINARY_EXPR", expr.toString());
        return new StringLiteralExpr(nameMap.get(expr.toString()));
    }

    public StringLiteralExpr visit(IntegerLiteralExpr expr, Void arg) {
        putSymbol("INTEGER_EXPR", expr.toString());
        return new StringLiteralExpr(nameMap.get(expr.toString()));
    }

    private void putSymbol(String type, String oldName) {
        int num = 1;
        if (numberMap.containsKey(type)) {
            num = numberMap.get(type);
            num++;
            numberMap.put(type, num);
        } else {
            numberMap.put(type, 1);
        }
        String newName = type.toLowerCase() + num;
        nameMap.put(oldName, newName);
    }
}
