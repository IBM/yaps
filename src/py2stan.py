import ast
import inspect
from . import stan_ir as IR
import astor

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

    def visit_Module(self, node):
        assert len(node.body) == 1
        self.visit(node.body[0])
        return IR.Program([
            IR.FunctionsBlock(self.functions),
            IR.DataBlock(self.data),
            IR.TransformedDataBlock(self.transformed_data),
            IR.ParametersBlock(self.parameters),
            IR.TransformedParametersBlock(self.transformed_parameters),
            IR.GeneratedQuantities(self.generated_quantities)
        ])

    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            self.visit(arg)
        for stmt in node.body:
            self.visit(stmt)

    # TODO support the fully annotated syntax
    def visit_With(self, node):
        assert len(node.items) == 1
        kind = node.items[0].context_expr.id
        if kind == 'functions':
            self.functions.append(astor.to_source(node.body))
        elif kind == 'data':
            assert False, 'Not yet implemented'
        elif kind == 'transformed_data':
            assert False, 'Not yet implemented'
        elif kind == 'parameters':
            assert False, 'Not yet implemented'
        elif kind == 'transformed_parameters':
            assert False, 'Not yet implemented'
        elif kind == 'model':
            for stmt in node.body:
                self.model.append(self.visit(stmt))
        elif kind == 'generated_quantities':
            assert False, 'Not yet implemented'
        else:
            assert False, 'Unknown block statement'

    def visit_AnnAssign(self, node):
        assert node.value is None and node.simple == 1
        id = node.target.id
        ty, cstr, dims = self.visit_annotation(node.annotation)
        print('Adding Parameter', id)
        self.parameters.append(IR.VariableDecl(id, ty, cstr, dims))

    def visit_arg(self, node):
        id = node.arg
        ty, cstr, dims = self.visit_annotation(node.annotation)
        print('Adding data', astor.to_source(node))
        self.data.append(IR.VariableDecl(id, ty, cstr, dims))

    def visit_annotation(self, node):
        if isinstance(node, ast.Subscript):
            type_ast = node.value
            dims = node.slice.value.n
        else:
            type_ast = node
            dims = None
        if isinstance(type_ast, ast.Call):
            ty = type_ast.func.id
            cstr = []
            for c in type_ast.keywords:
                cstr.append(self.visit_constraint(c))
        else:
            ty = astor.to_source(type_ast).strip()
        return ty, cstr, dims

    def visit_constraint(self, node):
        lhs = node.arg
        rhs = astor.to_source(node.value).strip()[1:-1]
        return '{}={}'.format(lhs, rhs)

    # Debug utils
    def print_parameters(self):
        for p in self.parameters:
            c = ', '.join(map(str, p.cstr))
            print('param {}:{}<{}>[{}]'.format(p.id, p.ty, c, p.dims))

    def print_data(self):
        for p in self.data:
            c = ', '.join(map(str, p.cstr))
            print('data {}:{}<{}>[{}]'.format(p.id, p.ty, c, p.dims))


def parse_model(model):
    source = inspect.getsource(model)
    tree = ast.parse(source)
    visitor = PythonVisitor()
    visitor.visit(tree)
    print('*****************************')
    visitor.print_parameters()
    visitor.print_data()
