# Copyright 2018 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        raise SyntaxError

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
            elif isinstance(stmt, ast.FunctionDef):
                self.functions.append(self.visit(stmt))
            elif not isinstance(stmt, ast.Pass):
                log('Model:\n', astor.to_source(stmt))
                self.model.append(self.visit(stmt))

    def visit_Block(self, node):
        assert len(node.items) == 1
        kind = node.items[0].context_expr.id
        if kind == 'functions':
            for stmt in node.body:
                f = self.visit(stmt)
                self.functions.append(f)
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
        elif kind == 'block':
            self.model.append(self.visit(node))
        else:
            assert False, 'Unknown block statement'

    def visit_DataDecl(self, node):
        id = node.arg
        ty = self.visit_datatype(node.annotation)
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
            ty = self.visit_datatype(type_ast.left)
            self.parameters.append(IR.VariableDecl(id, ty).set_map(node))
            dist, trunc = self.visit_distribution(type_ast.comparators[0])
            self.model.append(IR.SamplingStmt(
                IR.Variable(id), dist, trunc).set_map(node))
        else:
            ty = self.visit_datatype(node.annotation)
            self.parameters.append(IR.VariableDecl(id, ty).set_map(node))

    def visit_distribution(self, node):
        if isinstance(node, ast.Subscript):
            assert isinstance(node.value, ast.Attribute)
            assert node.value.attr == 'T'
            dist = self.visit(node.value.value)
            trunc = self.visit(node.slice)
            return dist, trunc
        else:
            return self.visit(node), None

    def visit_Attribute(self, node):
        assert node.attr == 'transpose', "We only support the transpose attribute"
        val = self.visit(node.value)
        return IR.Transpose(val)

    def visit_type(self, node):
        kind = None
        dims = None

        n = node

        if isinstance(n, ast.Subscript):
            dims = self.visit(n.slice.value)
            n = n.value

        if isinstance(n, ast.Name):
            kind = n.id
        else:
            assert False, 'Wrong type format'
        return IR.Type(kind, dims)

    def visit_datatype(self, node):
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
            assert False, 'Wrong data type format'

        if kind in ["int", "real"]:
            assert not inner_dims, ('Wrong data type format {} does not take a dimension'.format(
                kind))
            t = IR.AtomicDataType(kind, cstrts)
            if dims:
                return IR.ArrayDataType(t, dims)
            else:
                return t
        else:
            assert dims, ('Wrong data type format; {} requires a dimension'.format(
                kind))

            if inner_dims:
                return IR.ArrayDataType(IR.DimDataType(kind, inner_dims, cstrts), dims)
            else:
                return IR.DimDataType(kind, dims, cstrts)

    def visit_constraint(self, node):
        lhs = node.arg
        rhs = self.visit(node.value)
        return lhs, rhs

    # Python visitor
    def visit_FunctionDef(self, node):
        id = node.name
        ty = self.visit_type(node.returns)
        args = []
        for a in node.args.args:
            args.append(self.visit(a))
        body = []
        for stmt in node.body:
            s = self.visit(stmt)
            # Required because visit_Pass is not working
            if s is not None:
                body.append(s)
        return IR.FunctionDef(id, args, ty, body)

    def visit_arg(self, node):
        id = node.arg
        ty = self.visit_type(node.annotation)
        return IR.Arg(id, ty).set_map(node)

    def visit_Assign(self, node):
        assert len(node.targets) == 1
        lhs = self.visit(node.targets[0])
        rhs = self.visit(node.value)
        return IR.AssignStmt(lhs, None, rhs).set_map(node)

    def visit_AnnAssign(self, node):
        assert node.simple == 1
        id = node.target.id
        ty = self.visit_datatype(node.annotation)
        val = self.visit(node.value)
        return IR.VariableDecl(id, ty, val).set_map(node)

    def visit_AugAssign(self, node):
        lhs = self.visit(node.target)
        rhs = self.visit(node.value)
        return IR.AugAssignStmt(lhs, rhs).set_map(node)

    def visit_For(self, node):
        var = self.visit(node.target)
        iter = self.visit(node.iter)
        body = self.visit(node.body)
        return IR.ForStmt(var, iter, body).set_map(node)

    def visit_While(self, node):
        test = self.visit(node.test)
        body = self.visit(node.body)
        return IR.WhileStmt(test, body)

    def visit_If(self, node):
        cond = self.visit(node.test)
        exp = self.visit(node.body)
        alt = self.visit(node.orelse)
        return IR.ConditionalStmt(cond, exp, alt).set_map(node)

    def visit_With(self, node):
        body = self.visit(node.body)
        return IR.Block(body)

    def visit_Continue(self, node):
        return IR.ContinueStmt()

    def visit_Break(self, node):
        return IR.BreakStmt()

    def visit_Pass(self, node):
        return IR.PassStmt()

    def visit_Return(self, node):
        val = self.visit(node.value)
        return IR.ReturnStmt(val)

    def visit_Expr(self, node):
        body = self.visit(node.value)
        # `is` (ast.Compare) is used for the sampling statement
        if isinstance(node.value, ast.Compare):
            return body
        else:
            return IR.ExprStmt(body)

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

    def visit_List(self, node):
        elts = []
        for e in node.elts:
            elts.append(self.visit(e))
        return IR.List(elts)

    def visit_Set(self, node):
        elts = []
        for e in node.elts:
            elts.append(self.visit(e))
        return IR.Set(elts)

    def visit_Str(self, node):
        return IR.Constant(node.s).set_map(node)

    def visit_Slice(self, node):
        assert not node.step, "slices with a step not currently supported"
        lower = None
        upper = None
        if node.lower:
            lower = self.visit(node.lower)
        if node.upper:
            upper = self.visit(node.upper)
        return IR.Slice(lower, upper).set_map(node)

    def visit_ExtSlice(self, node):
        dims = []
        for e in node.dims:
            dims.append(self.visit(e))
        return IR.Tuple(dims).set_map(node)

    def visit_Subscript(self, node):
        val = self.visit(node.value)
        slice = self.visit(node.slice)
        return IR.Subscript(val, slice).set_map(node)

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Call(self, node):
        args = self.visit(node.args)
        if isinstance(node.func, ast.Name):
            id = node.func.id
            return IR.Call(id, args).set_map(node)
        elif isinstance(node.func, ast.Attribute):
            assert len(args) == 1, 'Wrong number of arguments'
            e2 = args[0]
            e1 = self.visit(node.func.value)
            if node.func.attr == 'pmult':
                return IR.Binop(IR.PMULT(), e1, e2)
            elif node.func.attr == 'pdiv':
                return IR.Binop(IR.PDIV(), e1, e2)
            else:
                assert False, 'Unsupported attribute method'
        else:
            assert False, 'Unsupported function call'

    def visit_Compare(self, node):
        # No chaining
        assert len(node.ops) == 1
        assert len(node.comparators) == 1
        op = node.ops[0]
        lhs = self.visit(node.left)
        # Is is the sampling operator
        if isinstance(op, ast.Is):
            dist, trunc = self.visit_distribution(node.comparators[0])
            return IR.SamplingStmt(lhs, dist, trunc).set_map(node)
        else:
            rhs = self.visit(node.comparators[0])
            op = self.visit(op)
            return IR.Binop(op, lhs, rhs).set_map(node)

    def visit_IfExp(self, node):
        test = self.visit(node.test)
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        return IR.IfExp(test, body, orelse).set_map(node)

    def visit_BinOp(self, node):
        op = self.visit(node.op)
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        return IR.Binop(op, lhs, rhs).set_map(node)

    def visit_UnaryOp(self, node):
        op = self.visit(node.op)
        expr = self.visit(node.operand)
        return IR.Unop(op, expr).set_map(node)

    def visit_BoolOp(self, node):
        op = self.visit(node.op)
        values = []
        for e in node.values:
            values.append(self.visit(e))
        return IR.Boolop(op, values)

    def visit_NameConstant(self, node):
        if node.value == True:
            return IR.Constant("true")
        elif node.value == False:
            return IR.Constant("true")
        else:
            assert False, 'None is not supported'

    def visit_USub(self, node):
        return IR.SUB()

    def visit_UAdd(self, node):
        return IR.ADD()

    def visit_Sub(self, node):
        return IR.SUB()

    def visit_Add(self, node):
        return IR.ADD()

    def visit_Mult(self, node):
        return IR.MULT()

    def visit_Div(self, node):
        return IR.DIV()

    def visit_Pow(self, node):
        return IR.POW()

    def visit_Mod(self, node):
        return IR.MOD()

    def visit_BitOr(self, node):
        return IR.MID()

    def visit_Eq(self, node):
        return IR.EQ()

    def visit_NotEq(self, node):
        return IR.NEQ()

    def visit_Lt(self, node):
        return IR.LT()

    def visit_LtE(self, node):
        return IR.LEQ()

    def visit_Gt(self, node):
        return IR.GT()

    def visit_GtE(self, node):
        return IR.GEQ()

    def visit_And(self, node):
        return IR.AND()

    def visit_Or(self, node):
        return IR.OR()

    def visit_Not(self, node):
        return IR.NOT()


def parse_string(s):
    # Hack to avoid weird AST with sampling op
    source = re.sub(r"<\s*~", "is", s, re.X)
    tree = ast.parse(source)
    visitor = PythonVisitor()
    return visitor.visit(tree)


def parse_function(model):
    source = inspect.getsource(model)
    return parse_string(source)
