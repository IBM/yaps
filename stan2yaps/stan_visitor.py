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


class Printer(stanListener):
    def __init__(self):
        self.indentation = 0

    def exitVariableDecl(self, ctx):
        vid = ctx.IDENTIFIER().getText()
        dims = ctx.arrayDim().ast if ctx.arrayDim() is not None else []
        ctx.ast = Assign(
            targets=[Name(id=vid, ctx=Store())],
            value=Call(func=Attribute(
                value=Name(id='torch', ctx=Load()),
                attr='zeros', ctx=Load()),
                args=[List(elts=dims, ctx=Load())],
                keywords=[]))

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
        if ctx.PLUS_EQ() is not None:
            assert False, 'Not yet implemented'
        elif ctx.truncation() is not None:
            assert False, 'Not yet implemented'
        else:
            id = ctx.IDENTIFIER()[0].getText()
            if hasattr(torch.distributions, id.capitalize()):
                # Check if the distribution exists in torch.distributions
                id = id.capitalize()
            exprList = ctx.expressionCommaList().ast
            ctx.ast = Assign(
                targets=[lvalue],
                value=Call(func=Attribute(
                    value=Call(
                        func=Name(id=id, ctx=Load()),
                        args=exprList,
                        keywords=[]),
                    attr='sample',
                    ctx=Load()),
                    args=[],
                    keywords=[]))

    # For loops (section 5.4)

    def exitForStmt(self, ctx):
        id = ctx.IDENTIFIER().getText()
        body = ctx.statement().ast if hasattr(ctx.statement(), 'ast') else []
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
                body=[body],
                orelse=[])

    # Conditional statements (section 5.5)

    def exitConditionalStmt(self, ctx):
        expr = ctx.expression().ast
        orstmt = [ctx.s2.ast] if ctx.s2 is not None else []
        ctx.ast = If(
            test=expr,
            body=[ctx.s1.ast],
            orelse=orstmt,
        )

    # While loops (section 5.6)

    def exitWhileStmt(self, ctx):
        expr = ctx.expression().ast
        stmt = ctx.statement().ast
        ctx.ast = While(
            test=expr,
            body=[stmt],
            orelse=[],
        )

    # Blocks (section 5.7)

    def exitBlockStmt(self, ctx):
        body = gatherChildrenASTList(ctx)
        # Hack: Blocks do not exist in python, replaced by `if True: ...`
        ctx.ast = If(
            test=NameConstant(value=True),
            body=body,
            orelse=[],)

    # Functions calls (sections 5.9 and 5.10)

    def exitCallStmt(self, ctx):
        id = ctx.IDENTIFIER().getText()
        args = ctx.expressionOrStringCommaList().ast
        ctx.ast = Expr(
            value=Call(
                func=Name(id=id, ctx=Load()),
                args=args,
                keywords=[],))

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
        ctx.ast = gatherChildrenASTList(ctx)

    def exitParametersBlock(self, ctx):
        ctx.ast = gatherChildrenASTList(ctx)

    def exitModelBlock(self, ctx):
        ctx.ast = gatherChildrenASTList(ctx)

    def exitProgram(self, ctx):
        ctx.ast = Module()
        ctx.ast.body = [
            Import(names=[alias(name='torch', asname=None)]),
            ImportFrom(
                module='torch.distributions',
                names=[alias(name='*', asname=None)],
                level=0)]
        ctx.ast.body += gatherChildrenASTList(ctx)
        ast.fix_missing_locations(ctx.ast)

        astpretty.pprint(ctx.ast)
        print('\n-----------------\n')
        print(astor.to_source(ctx.ast))
        print('\n-----------------\n')
        exec(compile(ctx.ast, filename="<ast>", mode="exec"))
