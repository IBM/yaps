'''
 * Copyright 2018 IBM Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys
import ast
from ast import *
from antlr4 import *
from parser.stanLexer import stanLexer
from parser.stanParser import stanParser
from parser.stanListener import stanListener
import astor
import astpretty
import torch


def parseExpr(expr):
    node = ast.parse(expr).body[0].value
    return node


def gatherChildrenASTList(ctx):
    ast = []
    if ctx.children is not None:
        for child in ctx.children:
            if hasattr(child, 'ast') and child.ast is not None:
                ast += child.ast
        return ast


def gatherChildrenAST(ctx):
    ast = []
    if ctx.children is not None:
        for child in ctx.children:
            if hasattr(child, 'ast') and child.ast is not None:
                ast.append(child.ast)
        return ast


def idxFromExprList(exprList):
    if len(exprList) == 1:
        return exprList[0]
    else:
        return Tuple(
            elts=exprList,
            ctx=Load())


def listFromStmt(stmt):
    if isinstance(stmt.ast, Block):
        return stmt.ast.body
    else:
        return [stmt.ast]


class Block(object):
    # Dummy class for blocks that are not supported in python
    def __init__(self, body):
        self.body = body


class Stan2Astpy(stanListener):
    def __init__(self):
        self.indentation = 0
        self.ast = None

    def exitTypeConstraint(self, ctx):
        ctx.ast = keyword(
            arg=ctx.IDENTIFIER().getText(),
            value=ctx.atom().ast
        )

    def exitTypeConstraintList(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    def exitTypeConstraints(self, ctx):
        ctx.ast = ctx.typeConstraintList().ast

    def exitType_(self, ctx):
        # TODO VectorType MatrixType
        kind = ctx.primitiveType().getText()
        if ctx.typeConstraints() is None:
            ctx.ast = Name(id=kind, ctx=Load())
        else:
            constraints = ctx.typeConstraints().ast
            ctx.ast = Call(
                func=Name(id=kind, ctx=Load()),
                args=[],
                keywords=constraints
            )

    def exitVariableDecl(self, ctx):
        vid = ctx.IDENTIFIER().getText()
        val = None
        if ctx.arrayDim() is not None:
            dims = ctx.arrayDim().ast
            ty = Subscript(
                value=ctx.type_().ast,
                slice=idxFromExprList(dims),
                ctx=Load()
            )
        else:
            ty = ctx.type_().ast
        if ctx.expression() is not None:
            val = ctx.expression().ast
        ctx.ast = AnnAssign(
            target=Name(id=vid, ctx=Store()),
            annotation=ty,
            value=val,
            simple=1,
        )

    def exitArrayDim(self, ctx):
        ctx.ast = ctx.expressionCommaList().ast

    def exitVariableDeclsOpt(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    # Vector, matrix and array expressions (section 4.2)

    def exitAtom(self, ctx):
        ctx.ast = parseExpr(ctx.getText())

    def exitExpression(self, ctx):
        if ctx.TRANSPOSE_OP() is not None:
            assert False, "Not yet implemented"
        elif ctx.POW_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Pow(),
                right=ctx.e2.ast,)
        elif ctx.DOT_MULT_OP() is not None:
            # Mult on tensors
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Mult(),
                right=ctx.e2.ast)
        elif ctx.DOT_DIV_OP() is not None:
            # Div on tensors
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Div(),
                right=ctx.e2.ast)
        elif ctx.LEFT_DIV_OP() is not None:
            assert False, "Not yet implemented"
        elif ctx.AND_OP() is not None:
            ctx.ast = BoolOp(
                op=And(),
                values=[
                    ctx.e1.ast,
                    ctx.e2.ast])
        elif ctx.OR_OP() is not None:
            ctx.ast = BoolOp(
                op=Or(),
                values=[
                    ctx.e1.ast,
                    ctx.e2.ast])
        elif '?' in ctx.getText():
            ctx.ast = IfExp(
                test=ctx.e1.ast,
                body=ctx.e2.ast,
                orelse=ctx.e3.ast)
        else:
            # All other cases are similar to Python syntax
            ctx.ast = parseExpr(ctx.getText())

    def exitExpressionCommaList(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    def exitExpressionCommaListOpt(self, ctx):
        ctx.ast = gatherChildrenASTList(ctx)

    # Statements (section 5)

    # Assignment (section 5.1)

    def exitLvalue(self, ctx):
        id = ctx.IDENTIFIER().getText()
        if ctx.expressionCommaList() is not None:
            idx = idxFromExprList(ctx.expressionCommaList().ast)
            ctx.ast = Subscript(
                value=Name(id=id, ctx=Load()),
                slice=Index(value=idx),
                ctx=Store())
        else:
            ctx.ast = Name(id=id, ctx=Store())

    def exitAssignStmt(self, ctx):
        lvalue = ctx.lvalue().ast
        expr = ctx.expression().ast
        if ctx.op is not None:
            op = None
            if ctx.PLUS_EQ() is not None:
                op = Add()
            if ctx.MINUS_EQ() is not None:
                op = Sub()
            if ctx.MULT_EQ() or ctx.DOT_MULT_EQ() is not None:
                op = Mult()
            if ctx.DIV_EQ() or ctx.DOT_DIV_EQ() is not None:
                op = Div()
            ctx.ast = AugAssign(
                target=lvalue,
                op=op,
                value=expr)
        else:
            ctx.ast = Assign(
                targets=[lvalue],
                value=expr)

    # Sampling (section 5.3)

    def exitLvalueSampling(self, ctx):
        if ctx.lvalue() is not None:
            ctx.ast = ctx.lvalue().ast
        elif ctx.expression() is not None:
            ctx.ast = ctx.expression().ast
        else:
            assert False

    def exitSamplingStmt(self, ctx):
        lvalue = ctx.lvalueSampling().ast
        id = ctx.IDENTIFIER()[0].getText()
        exprList = ctx.expressionCommaList().ast
        if ctx.PLUS_EQ() is not None:
            id_cond = ctx.IDENTIFIER()[1].getText()
            ctx.ast = AugAssign(
                target=lvalue,
                op=Add(),
                value=Call(
                    func=Name(id=id, ctx=Load()),
                    args=[
                        BinOp(
                            left=Name(id=id_cond, ctx=Load()),
                            op=BitOr(),
                            right=idxFromExprList(exprList),
                        ),
                    ],
                    keywords=[],
                ),
            )
        else:
            if ctx.truncation() is not None:
                assert False, 'Not yet implemented'
            ctx.ast = Expr(
                Compare(
                    left=lvalue,
                    ops=[Is()],
                    comparators=[
                        Call(
                            func=Name(id=id, ctx=Load()),
                            args=exprList,
                            keywords=[],
                        ),
                    ],
                )
            )

    # For loops (section 5.4)

    def exitForStmt(self, ctx):
        id = ctx.IDENTIFIER().getText()
        body = listFromStmt(ctx.statement())
        if len(ctx.atom()) > 1:
            # Index in Stan start at 1...
            lbound = BinOp(
                left=ctx.atom()[0].ast,
                op=Sub(),
                right=Num(n=1))
            ubound = ctx.atom()[1].ast
            ctx.ast = For(
                target=Name(id=id, ctx=Store()),
                iter=Call(func=Name(
                    id='range', ctx=Load()),
                    args=[lbound, ubound],
                    keywords=[]),
                body=body,
                orelse=[])

    # Conditional statements (section 5.5)

    def exitConditionalStmt(self, ctx):
        expr = ctx.expression().ast
        body = listFromStmt(ctx.s1)
        orstmt = listFromStmt(ctx.s2)
        ctx.ast = If(
            test=expr,
            body=body,
            orelse=orstmt,
        )

    # While loops (section 5.6)

    def exitWhileStmt(self, ctx):
        expr = ctx.expression().ast
        body = listFromStmt(ctx.statement())
        ctx.ast = While(
            test=expr,
            body=body,
            orelse=[],
        )

    # Blocks (section 5.7)

    def exitBlockStmt(self, ctx):
        body = gatherChildrenASTList(ctx)
        ctx.ast = Block(body=body)

    # Functions calls (sections 5.9 and 5.10)

    def exitCallStmt(self, ctx):
        call = ctx.callExpr().ast
        ctx.ast = Expr(value=call)

    def exitCallExpr(self, ctx):
        id = ctx.IDENTIFIER().getText()
        args = ctx.expressionOrStringCommaList().ast
        ctx.ast = Call(
            func=Name(id=id, ctx=Load()),
            args=args,
            keywords=[])

    def exitExpressionOrString(self, ctx):
        if ctx.expression() is not None:
            ctx.ast = ctx.expression().ast
        else:
            ctx.ast = Str(s=ctx.getText())

    def exitExpressionOrStringCommaList(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    # statements

    def exitStatement(self, ctx):
        if ctx.assignStmt() is not None:
            ctx.ast = ctx.assignStmt().ast
        if ctx.samplingStmt() is not None:
            ctx.ast = ctx.samplingStmt().ast
        if ctx.forStmt() is not None:
            ctx.ast = ctx.forStmt().ast
        if ctx.conditionalStmt() is not None:
            ctx.ast = ctx.conditionalStmt().ast
        if ctx.whileStmt() is not None:
            ctx.ast = ctx.whileStmt().ast
        if ctx.blockStmt() is not None:
            ctx.ast = ctx.blockStmt().ast
        if ctx.callStmt() is not None:
            ctx.ast = ctx.callStmt().ast
        if ctx.BREAK() is not None:
            ctx.ast = Break()
        if ctx.CONTINUE() is not None:
            ctx.ast = Continue()

    def exitStatementsOpt(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    # Program blocks (section 6)

    def exitDataBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        ctx.ast = With(items=[
            withitem(
                context_expr=Name(id='data', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)

    def exitTransformedDataBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        ctx.ast = With(items=[
            withitem(
                context_expr=Name(id='transformed_data', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)

    def exitParametersBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        ctx.ast = With(items=[
            withitem(
                context_expr=Name(id='parameters', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)

    def exitTransformedParametersBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        ctx.ast = With(items=[
            withitem(
                context_expr=Name(id='transformed_parameters', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)

    def exitModelBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        ctx.ast = With(items=[
            withitem(
                context_expr=Name(id='model', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)

    def exitGeneratedQuantitiesBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        ctx.ast = With(items=[
            withitem(
                context_expr=Name(id='generated_quantities', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)

    def exitProgram(self, ctx):
        body = gatherChildrenAST(ctx)
        ctx.ast = Module(body=[
            FunctionDef(
                name='model',
                args=arguments(args=[],
                               vararg=None,
                               kwonlyargs=[],
                               kw_defaults=[],
                               kwarg=None,
                               defaults=[]),
                body=body,
                decorator_list=[Name(id='yaps.model', ctx=Load())],
                returns=None
            )])
        ast.fix_missing_locations(ctx.ast)
        self.ast = ctx.ast


def stream2parsetree(stream):
    lexer = stanLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = stanParser(stream)
    tree = parser.program()
    return tree


def parsetree2astpy(tree):
    stan2astpy = Stan2Astpy()
    walker = ParseTreeWalker()
    walker.walk(stan2astpy, tree)
    return stan2astpy.ast


def stan2astpy(stream):
    tree = stream2parsetree(stream)
    astpy = parsetree2astpy(tree)
    return astpy


def stan2astpyFile(filename):
    stream = FileStream(filename)
    return stan2astpy(stream)


def stan2astpyStr(str):
    stream = InputStream(str)
    return stan2astpy(stream)


def do_compile(code_string=None, code_file=None):
    if not (code_string or code_file) or (code_string and code_file):
        assert False, "Either string or file but not both must be provided."
    if code_string:
        ast_ = stan2astpyStr(code_string)
    else:
        ast_ = stan2astpyFile(code_file)
    return ast_


def main(argv):
    if (len(argv) <= 1):
        assert False, "File name expected"
    astpy = stan2astpyFile(argv[1])
    # astpretty.pprint(astpy)
    print('\n-----------------\n')
    print(astor.to_source(astpy))
    print('\n-----------------\n')
    # exec(compile(astpy, filename="<ast>", mode="exec"))


if __name__ == '__main__':
    ast_ = main(sys.argv)
