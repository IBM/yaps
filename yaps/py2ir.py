import ast
import inspect
from . import ir as IR
import astor
import re

# kind = astor.to_source(node.items[0])


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
        return IR.Program([
            IR.FunctionsBlock(self.functions),
            IR.DataBlock(self.data),
            IR.TransformedDataBlock(self.transformed_data),
            IR.ParametersBlock(self.parameters),
            IR.TransformedParametersBlock(self.transformed_parameters),
            IR.GeneratedQuantities(self.generated_quantities)
        ])

    def visit_Model(self, node):
        for arg in node.args.args:
            self.visit_DataDecl(arg)
        for stmt in node.body:
            if isinstance(stmt, ast.With):
                self.visit_Block(stmt)
            elif isinstance(stmt, ast.AnnAssign):
                self.visit_parameter(stmt)
            else:
                print('Model:\n', astor.to_source(stmt))
                self.model.append(self.visit(stmt))

    def visit_Block(self, node):
        assert len(node.items) == 1
        kind = node.items[0].context_expr.id
        if kind == 'functions':
            self.functions.append(astor.to_source(node.body))
        elif kind == 'data':
            for stmt in node.body:
                data = self.visit(stmt)
                print('Data:', id)
                self.data.append(data)
        elif kind == 'transformed_data':
            assert False, 'Not yet implemented'
        elif kind == 'parameters':
            for stmt in node.body:
                param = self.visit(stmt)
                print('Param:', param.id)
                self.parameters.append(param)
        elif kind == 'transformed_parameters':
            assert False, 'Not yet implemented'
        elif kind == 'model':
            for stmt in node.body:
                print('Model:\n', astor.to_source(stmt))
                self.model.append(self.visit(stmt))
        elif kind == 'generated_quantities':
            assert False, 'Not yet implemented'
        else:
            assert False, 'Unknown block statement'

    def visit_DataDecl(self, node):
        id = node.arg
        ty = self.visit_type(node.annotation)
        print('Data:', id)
        self.data.append(IR.VariableDecl(id, ty))

    def visit_parameter(self, node):
        id = node.target.id
        print('Param:', id)
        type_ast = node.annotation
        if isinstance(type_ast, ast.Compare):
            assert len(type_ast.ops) == 1
            assert isinstance(type_ast.ops[0], ast.Is)
            assert len(type_ast.comparators) == 1
            ty = self.visit_type(type_ast.left)
            sval = self.visit(type_ast.comparators[0])
            self.parameters.append(IR.VariableDecl(id, ty))
            print('Model:\n', id, 'is', astor.to_source(
                type_ast.comparators[0]))
            self.model.append(IR.SamplingStmt(IR.Variable(id), sval))
        else:
            ty = self.visit(node.annotation)
            self.parameters.append(IR.VariableDecl(id, ty))

    def visit_type(self, node):
        kind = None
        cstrts = []
        dims = None
        if isinstance(node, ast.Subscript):
            type_ast = node.value
            dims = node.slice.value.n
        else:
            type_ast = node
        if isinstance(type_ast, ast.Call):
            kind = type_ast.func.id
            for c in type_ast.keywords:
                cstrts.append(self.visit_constraint(c))
        else:
            assert False, 'Wrong type format'
        return IR.Type(kind, cstrts, dims)

    def visit_constraint(self, node):
        lhs = node.arg
        rhs = self.visit(node.value)
        return lhs, rhs

    # Python visitor

    def visit_AnnAssign(self, node):
        assert node.value is None and node.simple == 1
        id = node.target.id
        ty = self.visit_type(node.annotation)
        return IR.VariableDecl(id, ty)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Num(self, node):
        return IR.Constant(node.n)

    def visit_Name(self, node):
        return IR.Variable(node.id)

    def visit_NoneType(self, node):
        return None

    def visit_Subscript(self, node):
        val = self.visit(node.value)
        slice = self.visit(node.slice)
        return IR.Subscript(val, slice)

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Call(self, node):
        id = node.func.id
        args = self.visit(node.args)
        return IR.Call(id, args)

    def visit_Compare(self, node):
        # No chaining
        assert len(node.ops) == 1
        assert len(node.comparators) == 1
        op = node.ops[0]
        lhs = self.visit(node.left)
        rhs = self.visit(node.comparators[0])
        # Is is the sampling operator
        if isinstance(op, ast.Is):
            return IR.SamplingStmt(lhs, rhs)
        else:
            op = self.visit(op)
            return IR.Binop(op, lhs, rhs)

    def visit_For(self, node):
        var = self.visit(node.target)
        iter = self.visit(node.iter)
        body = self.visit(node.body)
        return IR.ForStmt(var, iter, body)


def parse_model(model):
    source = inspect.getsource(model)
    # Hack to avoid weird AST with sampling op
    source = re.sub(r"<\s*~", "is", source, re.X)
    tree = ast.parse(source)
    visitor = PythonVisitor()
    visitor.visit(tree)
