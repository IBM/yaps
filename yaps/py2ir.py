import ast
import inspect
from . import ir as IR
import astor
import re


debug = False


def log(*args):
    if debug:
        print(*args)


class PythonVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.data = []
        self.transformed_data = []
        self.parameters = []
        self.transformed_parameters = []
        self.model = []
        self.generated_quantities = []

    def generic_visit(self, node):
        kind = type(node).__name__
        print("Missing visit method for {}".format(kind))

    def visit_list(self, list):
        res = []
        for item in list:
            res.append(self.visit(item))
        return res

    # Stan specifics
    def visit_Module(self, node):
        assert len(node.body) == 1
        model = node.body[0]
        assert isinstance(model, ast.FunctionDef), 'Model must be FunctionDecl'
        self.visit_Model(model)
        return IR.Program({
            "functions": IR.FunctionsBlock(self.functions),
            "data": IR.DataBlock(self.data),
            "transformed_data": IR.TransformedDataBlock(self.transformed_data),
            "parameters": IR.ParametersBlock(self.parameters),
            "transformed_parameters": IR.TransformedParametersBlock(self.transformed_parameters),
            "generated_quantities": IR.GeneratedQuantities(self.generated_quantities),
            "model": IR.ModelBlock(self.model),
        })

    def visit_Model(self, node):
        for arg in node.args.args:
            self.visit_DataDecl(arg)
        for stmt in node.body:
            if isinstance(stmt, ast.With):
                self.visit_Block(stmt)
            elif isinstance(stmt, ast.AnnAssign):
                self.visit_parameter(stmt)
            else:
                log('Model:\n', astor.to_source(stmt))
                self.model.append(self.visit(stmt))

    def visit_Block(self, node):
        assert len(node.items) == 1
        kind = node.items[0].context_expr.id
        if kind == 'functions':
            self.functions.append(astor.to_source(node.body))
        elif kind == 'data':
            for stmt in node.body:
                data = self.visit(stmt)
                log('Data:', id)
                self.data.append(data)
        elif kind == 'transformed_data':
            for stmt in node.body:
                log('T_Data:\n', astor.to_source(stmt))
                self.transformed_data.append(self.visit(stmt))
        elif kind == 'parameters':
            for stmt in node.body:
                param = self.visit(stmt)
                log('Param:', param.id)
                self.parameters.append(param)
        elif kind == 'transformed_parameters':
            for stmt in node.body:
                log('T_Param:\n', astor.to_source(stmt))
                self.transformed_parameters.append(self.visit(stmt))
        elif kind == 'model':
            for stmt in node.body:
                log('Model:\n', astor.to_source(stmt))
                self.model.append(self.visit(stmt))
        elif kind == 'generated_quantities':
            for stmt in node.body:
                log('G_Quant:\n', astor.to_source(stmt))
                self.generated_quantities.append(self.visit(stmt))
        else:
            assert False, 'Unknown block statement'

    def visit_DataDecl(self, node):
        id = node.arg
        ty = self.visit_type(node.annotation)
        log('Data:', id)
        self.data.append(IR.VariableDecl(id, ty).set_map(node))

    def visit_parameter(self, node):
        id = node.target.id
        log('Param:', id)
        type_ast = node.annotation
        if isinstance(type_ast, ast.Compare):
            assert len(type_ast.ops) == 1
            assert isinstance(type_ast.ops[0], ast.Is)
            assert len(type_ast.comparators) == 1
            ty = self.visit_type(type_ast.left)
            sval = self.visit(type_ast.comparators[0])
            self.parameters.append(IR.VariableDecl(id, ty).set_map(node))
            log('Model:\n', id, 'is', astor.to_source(type_ast.comparators[0]))
            self.model.append(IR.SamplingStmt(
                IR.Variable(id), sval).set_map(node))
        else:
            ty = self.visit(node.annotation)
            self.parameters.append(IR.VariableDecl(id, ty).set_map(node))

    def visit_type(self, node):
        kind = None
        cstrts = []
        dims = None
        inner_dims = None
        if isinstance(node, ast.Subscript):
            dims = self.visit(node.slice.value)
            type_ast = node.value
            if isinstance(type_ast, ast.Subscript):
                inner_dims = self.visit(type_ast.slice.value)
                type_ast = type_ast.value
        else:
            type_ast = node
        if isinstance(type_ast, ast.Name):
            kind = type_ast.id
        elif isinstance(type_ast, ast.Call):
            kind = type_ast.func.id
            for c in type_ast.keywords:
                cstrts.append(self.visit_constraint(c))
        else:
            assert False, 'Wrong type format'

        if kind in ["int", "real"]:
            assert not inner_dims, ('Wrong type format {} does not take a dimension'.format(kind))
            t = IR.AtomicType(kind, cstrts)
            if dims:
                return IR.ArrayType(t, dims)
            else:
                return t
        else:
            assert dims, ('Wrong type format; {} requires a dimension'.format(kind))

            if inner_dims:
                return IR.ArrayType(IR.DimType(kind, inner_dims, cstrts), dims)
            else:
                return IR.DimType(kind, dims, cstrts)

    def visit_constraint(self, node):
        lhs = node.arg
        rhs = self.visit(node.value)
        return lhs, rhs

    # Python visitor

    def visit_AnnAssign(self, node):
        assert node.simple == 1
        id = node.target.id
        ty = self.visit_type(node.annotation)
        val = self.visit(node.value)
        return IR.VariableDecl(id, ty, val).set_map(node)

    def visit_For(self, node):
        var = self.visit(node.target)
        iter = self.visit(node.iter)
        body = self.visit(node.body)
        return IR.ForStmt(var, iter, body).set_map(node)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Num(self, node):
        return IR.Constant(node.n).set_map(node)

    def visit_Name(self, node):
        return IR.Variable(node.id).set_map(node)

    def visit_NoneType(self, node):
        return None

    def visit_Tuple(self, node):
        elts = []
        for e in node.elts:
            elts.append(self.visit(e))
        return IR.Tuple(elts)

    def visit_Subscript(self, node):
        val = self.visit(node.value)
        slice = self.visit(node.slice)
        return IR.Subscript(val, slice).set_map(node)

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Call(self, node):
        id = node.func.id
        args = self.visit(node.args)
        return IR.Call(id, args).set_map(node)

    def visit_Compare(self, node):
        # No chaining
        assert len(node.ops) == 1
        assert len(node.comparators) == 1
        op = node.ops[0]
        lhs = self.visit(node.left)
        rhs = self.visit(node.comparators[0])
        # Is is the sampling operator
        if isinstance(op, ast.Is):
            return IR.SamplingStmt(lhs, rhs).set_map(node)
        else:
            op = self.visit(op)
            return IR.Binop(op, lhs, rhs).set_map(node)

    def visit_BinOp(self, node):
        op = self.visit(node.op)
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        return IR.Binop(op, lhs, rhs).set_map(node)

    def visit_UnaryOp(self, node):
        op = self.visit(node.op)
        expr = self.visit(node.operand)
        return IR.Unop(op, expr).set_map(node)

    def visit_USub(self, node):
        return IR.SUB()

    def visit_Sub(self, node):
        return IR.SUB()

    def visit_Add(self, node):
        return IR.ADD()

    def visit_Mult(self, node):
        return IR.MULT()

    def visit_Div(self, node):
        return IR.DIV()

    def visit_Mod(self, node):
        return IR.MOD()


def parse_model(model):
    source = inspect.getsource(model)
    # Hack to avoid weird AST with sampling op
    source = re.sub(r"<\s*~", "is", source, re.X)
    tree = ast.parse(source)
    visitor = PythonVisitor()
    return visitor.visit(tree)
