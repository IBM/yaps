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

import sys
import ast
from ast import *
from antlr4 import *
from .stanLexer import stanLexer
from .stanParser import stanParser
from .stanListener import stanListener
import astor
from antlr4.error.ErrorListener import ErrorListener

verbose = False


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
    if exprList is None:
        exprList = []
    if len(exprList) == 1:
        return exprList[0]
    else:
        return Tuple(
            elts=exprList,
            ctx=Load())


def isBlock(stmt):
    if isinstance(stmt.ast, With):
        expr = stmt.ast.items[0].context_expr
        if isinstance(expr, Name):
            return expr.id == 'block'
        else:
            return False
    else:
        return False


def listFromStmt(stmt):
    if isBlock(stmt):
        return stmt.ast.body
    else:
        return [stmt.ast]


def argsFromVardecl(vdecls):
    args = []
    for v in vdecls:
        assert (v.value is None)
        assert isinstance(v.target, Name)
        args.append(arg(arg=v.target.id, annotation=v.annotation))
    return args


def sliceFromExpr(e):
    if e is None:
        return Slice(lower=None, upper=None, step=None)
    else:
        return Index(value=e.ast)


class Stan2Astpy(stanListener):
    def __init__(self):
        self.data = []

    def exitTypeConstraint(self, ctx):
        ctx.ast = keyword(
            arg=ctx.IDENTIFIER().getText(),
            value=ctx.constraintExpression().ast
        )

    def exitTypeConstraintList(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    def exitTypeConstraints(self, ctx):
        ctx.ast = ctx.typeConstraintList().ast

    def exitType_(self, ctx):
        kind = None
        if ctx.primitiveType() is not None:
            kind = ctx.primitiveType().getText()
        elif ctx.vectorType() is not None:
            kind = ctx.vectorType().getText()
        elif ctx.matrixType() is not None:
            kind = ctx.matrixType().getText()
        else:
            assert False, "Internal error on " + ctx.getText()
        ty = None
        if ctx.typeConstraints() is None:
            ty = Name(id=kind, ctx=Load())
        else:
            constraints = ctx.typeConstraints().ast
            ty = Call(
                func=Name(id=kind, ctx=Load()),
                args=[],
                keywords=constraints
            )
        if ctx.arrayDim() is not None:
            dims = ctx.arrayDim().ast
            ctx.ast = Subscript(
                value=ty,
                slice=idxFromExprList(dims),
                ctx=Load()
            )
        else:
            ctx.ast = ty

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
        if ctx.expressionCommaListOpt() is not None:
            ctx.ast = ctx.expressionCommaListOpt().ast
        elif ctx.commaListOpt() is not None:
            ctx.ast = ctx.commaListOpt().ast
        else:
            assert False, "Internal error on " + ctx.getText()

    def exitCommaListOpt(self, ctx):
        ctx.ast = []
        if ctx.children is not None:
            for _ in range(len(ctx.children)):
                ctx.ast.append(Name(id='_', ctx=Store()))


    def exitVariableDeclsOpt(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    # Vector, matrix and array expressions (section 4.2)

    def exitVectorExpr(self, ctx):
        ctx.ast = List(elts=ctx.expressionCommaList().ast, ctx=Load())

    def exitArrayExpr(self, ctx):
        ctx.ast = Set(elts=ctx.expressionCommaList().ast, ctx=Load())

    def exitAtom(self, ctx):
        if ctx.constant() is not None:
            ctx.ast = parseExpr(ctx.getText())
        elif ctx.variable() is not None:
            ctx.ast = parseExpr(ctx.getText())
        elif ctx.vectorExpr() is not None:
            ctx.ast = ctx.vectorExpr().ast
        elif ctx.arrayExpr() is not None:
            ctx.ast = ctx.arrayExpr().ast
        elif ctx.arrayAccess is not None:
            if ctx.indexExpressionCommaListOpt() is not None:
                ctx.ast = Subscript(
                    value=ctx.arrayAccess.ast,
                    slice=ctx.indexExpressionCommaListOpt().ast,
                    ctx=Store())
            else:
                ctx.ast = Subscript(
                    value=ctx.arrayAccess.ast,
                    slice=Slice(lower=None, upper=None, step=None),
                    ctx=Store())
        elif ctx.callExpr() is not None:
            ctx.ast = ctx.callExpr().ast
        elif ctx.paren is not None:
            ctx.ast = ctx.expression().ast
        else:
            assert False, "Internal error on " + ctx.getText()

    def exitExpression(self, ctx):
        if ctx.atom() is not None:
            ctx.ast = ctx.atom().ast
        elif ctx.TRANSPOSE_OP() is not None:
            ctx.ast = Attribute(
                value=ctx.e.ast,
                attr='transpose', ctx=Load())
        elif ctx.POW_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Pow(),
                right=ctx.e2.ast,)
        elif ctx.DOT_MULT_OP() is not None:
            # Mult on tensors
            ctx.ast = Call(
                func=Attribute(
                    value=ctx.e1.ast,
                    attr='pmult',
                    ctx=Load()),
                args=[ctx.e2.ast],
                keywords=[])
        elif ctx.DOT_DIV_OP() is not None:
            # Div on tensors
            ctx.ast = Call(
                func=Attribute(
                    value=ctx.e1.ast,
                    attr='pdiv',
                    ctx=Load()),
                args=[ctx.e2.ast],
                keywords=[])
        elif ctx.LEFT_DIV_OP() is not None:
            assert False, "Not yet implemented"
        elif ctx.MULT_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Mult(),
                right=ctx.e2.ast)
        elif ctx.DIV_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Div(),
                right=ctx.e2.ast)
        elif ctx.MOD_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Mod(),
                right=ctx.e2.ast)
        elif ctx.NOT_OP() is not None:
            ctx.ast = UnaryOp(
                op=Not(),
                operand=ctx.e.ast)
        elif ctx.PLUS_OP() is not None:
            if ctx.e1 is None:
                ctx.ast = UnaryOp(
                    op=UAdd(),
                    operand=ctx.e.ast)
            else:
                ctx.ast = BinOp(
                    left=ctx.e1.ast,
                    op=Add(),
                    right=ctx.e2.ast)
        elif ctx.MINUS_OP() is not None:
            if ctx.e1 is None:
                ctx.ast = UnaryOp(
                    op=USub(),
                    operand=ctx.e.ast)
            else:
                ctx.ast = BinOp(
                    left=ctx.e1.ast,
                    op=Sub(),
                    right=ctx.e2.ast)
        elif ctx.LT_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Lt(),
                right=ctx.e2.ast)
        elif ctx.LE_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=LtE(),
                right=ctx.e2.ast)
        elif ctx.GT_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Gt(),
                right=ctx.e2.ast)
        elif ctx.GE_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=GtE(),
                right=ctx.e2.ast)
        elif ctx.EQ_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Eq(),
                right=ctx.e2.ast)
        elif ctx.NEQ_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=NotEq(),
                right=ctx.e2.ast)
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
            assert False, "Internal error on " + ctx.getText()

    def exitConstraintExpression(self, ctx):
        if ctx.atom() is not None:
            ctx.ast = ctx.atom().ast
        elif ctx.TRANSPOSE_OP() is not None:
            ctx.ast = Attribute(
                value=ctx.e.ast,
                attr='transpose', ctx=Load())
        elif ctx.POW_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Pow(),
                right=ctx.e2.ast,)
        elif ctx.DOT_MULT_OP() is not None:
            # Mult on tensors
            ctx.ast = Call(
                func=Attribute(
                    value=ctx.e1.ast,
                    attr='pmult',
                    ctx=Load()),
                args=[ctx.e2.ast],
                keywords=[])
        elif ctx.DOT_DIV_OP() is not None:
            # Div on tensors
            ctx.ast = Call(
                func=Attribute(
                    value=ctx.e1.ast,
                    attr='pdiv',
                    ctx=Load()),
                args=[ctx.e2.ast],
                keywords=[])
        elif ctx.LEFT_DIV_OP() is not None:
            assert False, "Not yet implemented"
        elif ctx.MULT_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Mult(),
                right=ctx.e2.ast)
        elif ctx.DIV_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Div(),
                right=ctx.e2.ast)
        elif ctx.MOD_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Mod(),
                right=ctx.e2.ast)
        elif ctx.NOT_OP() is not None:
            ctx.ast = UnaryOp(
                op=Not(),
                operand=ctx.e.ast)
        elif ctx.PLUS_OP() is not None:
            if ctx.e1 is None:
                ctx.ast = UnaryOp(
                    op=UAdd(),
                    operand=ctx.e.ast)
            else:
                ctx.ast = BinOp(
                    left=ctx.e1.ast,
                    op=Add(),
                    right=ctx.e2.ast)
        elif ctx.MINUS_OP() is not None:
            if ctx.e1 is None:
                ctx.ast = UnaryOp(
                    op=USub(),
                    operand=ctx.e.ast)
            else:
                ctx.ast = BinOp(
                    left=ctx.e1.ast,
                    op=Sub(),
                    right=ctx.e2.ast)
        elif ctx.LT_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Lt(),
                right=ctx.e2.ast)
        elif ctx.LE_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=LtE(),
                right=ctx.e2.ast)
        elif ctx.EQ_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=Eq(),
                right=ctx.e2.ast)
        elif ctx.NEQ_OP() is not None:
            ctx.ast = BinOp(
                left=ctx.e1.ast,
                op=NotEq(),
                right=ctx.e2.ast)
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
            assert False, "Internal error on " + ctx.getText()

    def exitIndexExpression(self, ctx):
        if ctx.sliceOp is not None:
            lower = None
            if ctx.e1 is not None:
                lower = sliceFromExpr(ctx.e1)
            upper = None
            if ctx.e2 is not None:
                upper = sliceFromExpr(ctx.e2)
            ctx.ast = Slice(lower=lower,
                            upper=upper,
                            step=None)
        elif ctx.e is not None:
            ctx.ast = Index(value=ctx.e.ast)
        else:
            ctx.ast = Slice(lower=None,
                            upper=None,
                            step=None)

    def exitExpressionCommaList(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    def exitExpressionCommaListOpt(self, ctx):
        ctx.ast = gatherChildrenASTList(ctx)

    def exitIndexExpressionCommaListOpt(self, ctx):
        ctx.ast = Tuple(elts=gatherChildrenAST(ctx), ctx=Load())

    # Statements (section 5)

    # Assignment (section 5.1)

    def exitLvalue(self, ctx):
        id = ctx.IDENTIFIER().getText()
        if ctx.indexExpressionCommaListOpt() is not None:
            idx = idxFromExprList(ctx.indexExpressionCommaListOpt().ast.elts)
            ctx.ast = Subscript(
                value=Name(id=id, ctx=Load()),
                slice=Index(value=idx),
                ctx=Store())
        else:
            ctx.ast = Name(id=id, ctx=Store())

    def exitAssignStmt(self, ctx):
        if ctx.sample is not None:
            ctx.ast = Expr(
                Compare(
                    left=ctx.le.ast,
                    ops=[Is()],
                    comparators=[ctx.re.ast]))
        elif ctx.eq is not None:
            ctx.ast = Assign(
                targets=[ctx.lvalue().ast],
                value=ctx.e.ast)
        elif ctx.op:
            op = None
            if ctx.PLUS_EQ() is not None:
                op = Add()
            elif ctx.MINUS_EQ() is not None:
                op = Sub()
            if ctx.MULT_EQ() or ctx.DOT_MULT_EQ() is not None:
                op = Mult()
            if ctx.DIV_EQ() or ctx.DOT_DIV_EQ() is not None:
                op = Div()
            ctx.ast = AugAssign(
                target=ctx.lvalue().ast,
                op=op,
                value=ctx.e.ast)
        else:
            assert False, "Internal error on " + ctx.getText()

    # Sampling (section 5.3)

    def exitTruncation(self, ctx):
        if ctx.IDENTIFIER().getText() is not 'T':
            assert False, 'Syntax error'
        if ctx.e1 is None or ctx.e2 is None:
            ctx.ast = ExtSlice(
                dims=[
                    sliceFromExpr(ctx.e1),
                    sliceFromExpr(ctx.e2),
                ],
            )
        else:
            ctx.ast = Index(
                value=Tuple(
                    elts=[
                        ctx.e1.ast,
                        ctx.e2.ast,
                    ],
                    ctx=Load(),
                )
            )

    # For loops (section 5.4)

    def exitForStmt(self, ctx):
        id = ctx.IDENTIFIER().getText()
        body = listFromStmt(ctx.statement())
        iter = None
        if ctx.expression() is not None:
            lbound = ctx.atom().ast
            ubound = ctx.expression().ast
            iter = Call(func=Name(
                id='range', ctx=Load()),
                args=[lbound, ubound],
                keywords=[])
        else:
            iter = ctx.atom().ast
        ctx.ast = For(
            target=Name(id=id, ctx=Store()),
            iter=iter,
            body=body,
            orelse=[])
    # Conditional statements (section 5.5)

    def exitConditionalStmt(self, ctx):
        expr = ctx.expression().ast
        body = listFromStmt(ctx.s1)
        if ctx.s2 is not None:
            orstmt = listFromStmt(ctx.s2)
        else:
            orstmt = []
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
        if body == []:
            body = [ Pass() ]
        ctx.ast = With(items=[
            withitem(
                context_expr=Name(id='block', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)

    # Functions calls (sections 5.9 and 5.10)

    def exitCallStmt(self, ctx):
        call = ctx.callExpr().ast
        ctx.ast = Expr(value=call)

    def exitCallExpr(self, ctx):
        if ctx.f is not None:
            f = ctx.IDENTIFIER().getText()
            args = ctx.expressionOrStringCommaList().ast
            call = Call(
                func=Name(id=f, ctx=Load()),
                args=args,
                keywords=[])
            if ctx.truncation() is None:
                ctx.ast = call
            else:
                trunc = ctx.truncation().ast
                ctx.ast = Subscript(
                    value=Attribute(
                        value=call,
                        attr='T',
                        ctx=Load()),
                    slice=trunc,
                    ctx=Load())
        elif ctx.id1 is not None:
            id1 = ctx.IDENTIFIER().getText()
            expr = ctx.expression().ast
            exprList = ctx.expressionCommaList().ast
            ctx.ast = Call(
                func=Name(id=id1, ctx=Load()),
                args=[
                    BinOp(
                        left=expr,
                        op=BitOr(),
                        right=idxFromExprList(exprList),
                    ),
                ],
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
        elif ctx.forStmt() is not None:
            ctx.ast = ctx.forStmt().ast
        elif ctx.conditionalStmt() is not None:
            ctx.ast = ctx.conditionalStmt().ast
        elif ctx.whileStmt() is not None:
            ctx.ast = ctx.whileStmt().ast
        elif ctx.blockStmt() is not None:
            ctx.ast = ctx.blockStmt().ast
        elif ctx.callStmt() is not None:
            ctx.ast = ctx.callStmt().ast
        elif ctx.BREAK() is not None:
            ctx.ast = Break()
        elif ctx.CONTINUE() is not None:
            ctx.ast = Continue()
        elif ctx.returnStmt() is not None:
            ctx.ast = ctx.returnStmt().ast
        elif ctx.empty is not None:
            ctx.ast = Pass()
        else:
            assert False, "Internal error on " + ctx.getText()

    def exitStatementsOpt(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    # Functions (section 7)

    def exitFunctionDecl(self, ctx):
        name = ctx.IDENTIFIER().getText()
        args = ctx.parameterCommaListOpt().ast
        body = [ctx.statement().ast]
        # if ctx.statement().blockStmt() is not None:
        #     body = body.body
        # else:
        #     body = [body]
        returnType = ctx.unsizedReturnType().ast
        ctx.ast = FunctionDef(
            name=name,
            args=arguments(args=args,
                           vararg=None,
                           kwonlyargs=[],
                           kw_defaults=[],
                           kwarg=None,
                           defaults=[]),
            body=body,
            decorator_list=[],
            returns=returnType)



    def exitUnsizedReturnType(self, ctx):
        if ctx.VOID() is not None:
            ctx.ast = Name(id='void', ctx=Load())
        elif ctx.unsizedType() is not None:
            ctx.ast = ctx.unsizedType().ast
        else:
            assert False, "Internal error on " + ctx.getText()

    def exitUnsizedType(self, ctx):
        kind = ctx.basicType().getText()
        ty = Name(id=kind, ctx=Load())
        if ctx.unsizedDims() is not None:
            dims = ctx.unsizedDims().ast
            ctx.ast = Subscript(
                value=ty,
                slice=dims,
                ctx=Load()
            )
        else:
            ctx.ast = ty

    def exitUnsizedDims(self, ctx):
        elts = [ Tuple(elts=[], ctx=Load()) ]
        if ctx.commas is not None:
            elts += [Tuple(elts=[], ctx=Load()) for _ in ctx.commas]
        ctx.ast = Tuple(elts=elts, ctx=Load())

    # def exitFunctionType(self, ctx):
    #     name = ctx.IDENTIFIER().getText()
    #     args = ctx.parameterCommaListOpt().ast
    #     returnType = None
    #     if ctx.type_() is not None:
    #         returnType = ctx.type_().ast
    #     elif ctx.VOID() is not None:
    #         returnType = Name(id='void', ctx=Load())
    #     else:
    #         assert False, "Internal error on " + ctx.getText()
    #     ctx.ast = FunctionDef(
    #         name=name,
    #         args=arguments(args=args,
    #                        vararg=None,
    #                        kwonlyargs=[],
    #                        kw_defaults=[],
    #                        kwarg=None,
    #                        defaults=[]),
    #         body=[Pass()],
    #         decorator_list=[],
    #         returns=returnType)

    def exitParameterDecl(self, ctx):
        vid = ctx.IDENTIFIER().getText()
        ty = ctx.unsizedType().ast
        ctx.ast = arg(arg=vid, annotation=ty)

    def exitParameterCommaList(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    def exitParameterCommaListOpt(self, ctx):
        ctx.ast = gatherChildrenASTList(ctx)

    def exitReturnStmt(self, ctx):
        if ctx.expression() is None:
            ctx.ast = Return(value=None)
        else:
            ctx.ast = Return(value=ctx.expression().ast)

    def exitFunctionDeclsOpt(self, ctx):
        ctx.ast = gatherChildrenAST(ctx)

    # Program blocks (section 6)

    def exitFunctionBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        if len(body) == 0:
            body = [Pass()]
        ctx.ast = [With(items=[
            withitem(
                context_expr=Name(id='functions', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)]

    def exitDataBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        if verbose:
            ctx.ast = [With(items=[
                withitem(
                    context_expr=Name(id='data', ctx=Load()),
                    optional_vars=None,
                ),
            ], body=body)]
        else:
            self.data += body

    def exitTransformedDataBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        if len(body) == 0:
            body = [Pass()]
        ctx.ast = [With(items=[
            withitem(
                context_expr=Name(id='transformed_data', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)]

    def exitParametersBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        if len(body) == 0:
            body = [Pass()]
        if verbose:
            ctx.ast = [With(items=[
                withitem(
                    context_expr=Name(id='parameters', ctx=Load()),
                    optional_vars=None,
                ),
            ], body=body)]
        else:
            ctx.ast = body

    def exitTransformedParametersBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        if len(body) == 0:
            body = [Pass()]
        ctx.ast = [With(items=[
            withitem(
                context_expr=Name(id='transformed_parameters', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)]

    def exitModelBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        if len(body) == 0:
            body = [Pass()]
        if verbose or not (ctx.variableDeclsOpt().ast == []) or ctx.statement() is not None:
            ctx.ast = [With(items=[
                withitem(
                    context_expr=Name(id='model', ctx=Load()),
                    optional_vars=None,
                ),
            ], body=body)]
        else:
            ctx.ast = body

    def exitGeneratedQuantitiesBlock(self, ctx):
        body = gatherChildrenASTList(ctx)
        if len(body) == 0:
            body = [Pass()]
        ctx.ast = [With(items=[
            withitem(
                context_expr=Name(id='generated_quantities', ctx=Load()),
                optional_vars=None,
            ),
        ], body=body)]

    def exitProgram(self, ctx):
        body = gatherChildrenASTList(ctx)
        if len(body) == 0:
            body = [Pass()]
        ctx.ast = Module(body=[
            FunctionDef(
                name='stan_model',
                args=arguments(args=argsFromVardecl(self.data),
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


####################

class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print('Line ' + str(line) + ':' + str(column) +
              ': Syntax error, ' + str(msg))
        raise SyntaxError


def stream2parsetree(stream):
    lexer = stanLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = stanParser(stream)
    parser._listeners = [MyErrorListener()]
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


def from_stan(code_string=None, code_file=None):
    ast_ = do_compile(code_string, code_file)
    return astor.to_source(ast_)


def main():
    if (len(sys.argv) <= 1):
        assert False, "File name expected"
    for i in range(1, len(sys.argv)):
        print('# -------------')
        print('#', sys.argv[i])
        print('# -------------')
        code = from_stan(code_file=sys.argv[i])
        print(code)


if __name__ == '__main__':
    main()
