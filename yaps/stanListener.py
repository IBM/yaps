# Generated from yaps/stan.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .stanParser import stanParser
else:
    from stanParser import stanParser

# This class defines a complete listener for a parse tree produced by stanParser.
class stanListener(ParseTreeListener):

    # Enter a parse tree produced by stanParser#include.
    def enterInclude(self, ctx:stanParser.IncludeContext):
        pass

    # Exit a parse tree produced by stanParser#include.
    def exitInclude(self, ctx:stanParser.IncludeContext):
        pass


    # Enter a parse tree produced by stanParser#primitiveType.
    def enterPrimitiveType(self, ctx:stanParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by stanParser#primitiveType.
    def exitPrimitiveType(self, ctx:stanParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by stanParser#vectorType.
    def enterVectorType(self, ctx:stanParser.VectorTypeContext):
        pass

    # Exit a parse tree produced by stanParser#vectorType.
    def exitVectorType(self, ctx:stanParser.VectorTypeContext):
        pass


    # Enter a parse tree produced by stanParser#matrixType.
    def enterMatrixType(self, ctx:stanParser.MatrixTypeContext):
        pass

    # Exit a parse tree produced by stanParser#matrixType.
    def exitMatrixType(self, ctx:stanParser.MatrixTypeContext):
        pass


    # Enter a parse tree produced by stanParser#type_.
    def enterType_(self, ctx:stanParser.Type_Context):
        pass

    # Exit a parse tree produced by stanParser#type_.
    def exitType_(self, ctx:stanParser.Type_Context):
        pass


    # Enter a parse tree produced by stanParser#typeConstraints.
    def enterTypeConstraints(self, ctx:stanParser.TypeConstraintsContext):
        pass

    # Exit a parse tree produced by stanParser#typeConstraints.
    def exitTypeConstraints(self, ctx:stanParser.TypeConstraintsContext):
        pass


    # Enter a parse tree produced by stanParser#typeConstraintList.
    def enterTypeConstraintList(self, ctx:stanParser.TypeConstraintListContext):
        pass

    # Exit a parse tree produced by stanParser#typeConstraintList.
    def exitTypeConstraintList(self, ctx:stanParser.TypeConstraintListContext):
        pass


    # Enter a parse tree produced by stanParser#typeConstraint.
    def enterTypeConstraint(self, ctx:stanParser.TypeConstraintContext):
        pass

    # Exit a parse tree produced by stanParser#typeConstraint.
    def exitTypeConstraint(self, ctx:stanParser.TypeConstraintContext):
        pass


    # Enter a parse tree produced by stanParser#variableDecl.
    def enterVariableDecl(self, ctx:stanParser.VariableDeclContext):
        pass

    # Exit a parse tree produced by stanParser#variableDecl.
    def exitVariableDecl(self, ctx:stanParser.VariableDeclContext):
        pass


    # Enter a parse tree produced by stanParser#arrayDim.
    def enterArrayDim(self, ctx:stanParser.ArrayDimContext):
        pass

    # Exit a parse tree produced by stanParser#arrayDim.
    def exitArrayDim(self, ctx:stanParser.ArrayDimContext):
        pass


    # Enter a parse tree produced by stanParser#commaListOpt.
    def enterCommaListOpt(self, ctx:stanParser.CommaListOptContext):
        pass

    # Exit a parse tree produced by stanParser#commaListOpt.
    def exitCommaListOpt(self, ctx:stanParser.CommaListOptContext):
        pass


    # Enter a parse tree produced by stanParser#variableDeclsOpt.
    def enterVariableDeclsOpt(self, ctx:stanParser.VariableDeclsOptContext):
        pass

    # Exit a parse tree produced by stanParser#variableDeclsOpt.
    def exitVariableDeclsOpt(self, ctx:stanParser.VariableDeclsOptContext):
        pass


    # Enter a parse tree produced by stanParser#constant.
    def enterConstant(self, ctx:stanParser.ConstantContext):
        pass

    # Exit a parse tree produced by stanParser#constant.
    def exitConstant(self, ctx:stanParser.ConstantContext):
        pass


    # Enter a parse tree produced by stanParser#variable.
    def enterVariable(self, ctx:stanParser.VariableContext):
        pass

    # Exit a parse tree produced by stanParser#variable.
    def exitVariable(self, ctx:stanParser.VariableContext):
        pass


    # Enter a parse tree produced by stanParser#vectorExpr.
    def enterVectorExpr(self, ctx:stanParser.VectorExprContext):
        pass

    # Exit a parse tree produced by stanParser#vectorExpr.
    def exitVectorExpr(self, ctx:stanParser.VectorExprContext):
        pass


    # Enter a parse tree produced by stanParser#arrayExpr.
    def enterArrayExpr(self, ctx:stanParser.ArrayExprContext):
        pass

    # Exit a parse tree produced by stanParser#arrayExpr.
    def exitArrayExpr(self, ctx:stanParser.ArrayExprContext):
        pass


    # Enter a parse tree produced by stanParser#atom.
    def enterAtom(self, ctx:stanParser.AtomContext):
        pass

    # Exit a parse tree produced by stanParser#atom.
    def exitAtom(self, ctx:stanParser.AtomContext):
        pass


    # Enter a parse tree produced by stanParser#callExpr.
    def enterCallExpr(self, ctx:stanParser.CallExprContext):
        pass

    # Exit a parse tree produced by stanParser#callExpr.
    def exitCallExpr(self, ctx:stanParser.CallExprContext):
        pass


    # Enter a parse tree produced by stanParser#expression.
    def enterExpression(self, ctx:stanParser.ExpressionContext):
        pass

    # Exit a parse tree produced by stanParser#expression.
    def exitExpression(self, ctx:stanParser.ExpressionContext):
        pass


    # Enter a parse tree produced by stanParser#constraintExpression.
    def enterConstraintExpression(self, ctx:stanParser.ConstraintExpressionContext):
        pass

    # Exit a parse tree produced by stanParser#constraintExpression.
    def exitConstraintExpression(self, ctx:stanParser.ConstraintExpressionContext):
        pass


    # Enter a parse tree produced by stanParser#indexExpression.
    def enterIndexExpression(self, ctx:stanParser.IndexExpressionContext):
        pass

    # Exit a parse tree produced by stanParser#indexExpression.
    def exitIndexExpression(self, ctx:stanParser.IndexExpressionContext):
        pass


    # Enter a parse tree produced by stanParser#expressionCommaList.
    def enterExpressionCommaList(self, ctx:stanParser.ExpressionCommaListContext):
        pass

    # Exit a parse tree produced by stanParser#expressionCommaList.
    def exitExpressionCommaList(self, ctx:stanParser.ExpressionCommaListContext):
        pass


    # Enter a parse tree produced by stanParser#expressionCommaListOpt.
    def enterExpressionCommaListOpt(self, ctx:stanParser.ExpressionCommaListOptContext):
        pass

    # Exit a parse tree produced by stanParser#expressionCommaListOpt.
    def exitExpressionCommaListOpt(self, ctx:stanParser.ExpressionCommaListOptContext):
        pass


    # Enter a parse tree produced by stanParser#indexExpressionCommaListOpt.
    def enterIndexExpressionCommaListOpt(self, ctx:stanParser.IndexExpressionCommaListOptContext):
        pass

    # Exit a parse tree produced by stanParser#indexExpressionCommaListOpt.
    def exitIndexExpressionCommaListOpt(self, ctx:stanParser.IndexExpressionCommaListOptContext):
        pass


    # Enter a parse tree produced by stanParser#lvalue.
    def enterLvalue(self, ctx:stanParser.LvalueContext):
        pass

    # Exit a parse tree produced by stanParser#lvalue.
    def exitLvalue(self, ctx:stanParser.LvalueContext):
        pass


    # Enter a parse tree produced by stanParser#assignStmt.
    def enterAssignStmt(self, ctx:stanParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by stanParser#assignStmt.
    def exitAssignStmt(self, ctx:stanParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by stanParser#truncation.
    def enterTruncation(self, ctx:stanParser.TruncationContext):
        pass

    # Exit a parse tree produced by stanParser#truncation.
    def exitTruncation(self, ctx:stanParser.TruncationContext):
        pass


    # Enter a parse tree produced by stanParser#forStmt.
    def enterForStmt(self, ctx:stanParser.ForStmtContext):
        pass

    # Exit a parse tree produced by stanParser#forStmt.
    def exitForStmt(self, ctx:stanParser.ForStmtContext):
        pass


    # Enter a parse tree produced by stanParser#conditionalStmt.
    def enterConditionalStmt(self, ctx:stanParser.ConditionalStmtContext):
        pass

    # Exit a parse tree produced by stanParser#conditionalStmt.
    def exitConditionalStmt(self, ctx:stanParser.ConditionalStmtContext):
        pass


    # Enter a parse tree produced by stanParser#whileStmt.
    def enterWhileStmt(self, ctx:stanParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by stanParser#whileStmt.
    def exitWhileStmt(self, ctx:stanParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by stanParser#blockStmt.
    def enterBlockStmt(self, ctx:stanParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by stanParser#blockStmt.
    def exitBlockStmt(self, ctx:stanParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by stanParser#callStmt.
    def enterCallStmt(self, ctx:stanParser.CallStmtContext):
        pass

    # Exit a parse tree produced by stanParser#callStmt.
    def exitCallStmt(self, ctx:stanParser.CallStmtContext):
        pass


    # Enter a parse tree produced by stanParser#expressionOrString.
    def enterExpressionOrString(self, ctx:stanParser.ExpressionOrStringContext):
        pass

    # Exit a parse tree produced by stanParser#expressionOrString.
    def exitExpressionOrString(self, ctx:stanParser.ExpressionOrStringContext):
        pass


    # Enter a parse tree produced by stanParser#expressionOrStringCommaList.
    def enterExpressionOrStringCommaList(self, ctx:stanParser.ExpressionOrStringCommaListContext):
        pass

    # Exit a parse tree produced by stanParser#expressionOrStringCommaList.
    def exitExpressionOrStringCommaList(self, ctx:stanParser.ExpressionOrStringCommaListContext):
        pass


    # Enter a parse tree produced by stanParser#statement.
    def enterStatement(self, ctx:stanParser.StatementContext):
        pass

    # Exit a parse tree produced by stanParser#statement.
    def exitStatement(self, ctx:stanParser.StatementContext):
        pass


    # Enter a parse tree produced by stanParser#statementsOpt.
    def enterStatementsOpt(self, ctx:stanParser.StatementsOptContext):
        pass

    # Exit a parse tree produced by stanParser#statementsOpt.
    def exitStatementsOpt(self, ctx:stanParser.StatementsOptContext):
        pass


    # Enter a parse tree produced by stanParser#functionDecl.
    def enterFunctionDecl(self, ctx:stanParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by stanParser#functionDecl.
    def exitFunctionDecl(self, ctx:stanParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by stanParser#unsizedReturnType.
    def enterUnsizedReturnType(self, ctx:stanParser.UnsizedReturnTypeContext):
        pass

    # Exit a parse tree produced by stanParser#unsizedReturnType.
    def exitUnsizedReturnType(self, ctx:stanParser.UnsizedReturnTypeContext):
        pass


    # Enter a parse tree produced by stanParser#unsizedType.
    def enterUnsizedType(self, ctx:stanParser.UnsizedTypeContext):
        pass

    # Exit a parse tree produced by stanParser#unsizedType.
    def exitUnsizedType(self, ctx:stanParser.UnsizedTypeContext):
        pass


    # Enter a parse tree produced by stanParser#basicType.
    def enterBasicType(self, ctx:stanParser.BasicTypeContext):
        pass

    # Exit a parse tree produced by stanParser#basicType.
    def exitBasicType(self, ctx:stanParser.BasicTypeContext):
        pass


    # Enter a parse tree produced by stanParser#unsizedDims.
    def enterUnsizedDims(self, ctx:stanParser.UnsizedDimsContext):
        pass

    # Exit a parse tree produced by stanParser#unsizedDims.
    def exitUnsizedDims(self, ctx:stanParser.UnsizedDimsContext):
        pass


    # Enter a parse tree produced by stanParser#parameterDecl.
    def enterParameterDecl(self, ctx:stanParser.ParameterDeclContext):
        pass

    # Exit a parse tree produced by stanParser#parameterDecl.
    def exitParameterDecl(self, ctx:stanParser.ParameterDeclContext):
        pass


    # Enter a parse tree produced by stanParser#parameterCommaList.
    def enterParameterCommaList(self, ctx:stanParser.ParameterCommaListContext):
        pass

    # Exit a parse tree produced by stanParser#parameterCommaList.
    def exitParameterCommaList(self, ctx:stanParser.ParameterCommaListContext):
        pass


    # Enter a parse tree produced by stanParser#parameterCommaListOpt.
    def enterParameterCommaListOpt(self, ctx:stanParser.ParameterCommaListOptContext):
        pass

    # Exit a parse tree produced by stanParser#parameterCommaListOpt.
    def exitParameterCommaListOpt(self, ctx:stanParser.ParameterCommaListOptContext):
        pass


    # Enter a parse tree produced by stanParser#returnStmt.
    def enterReturnStmt(self, ctx:stanParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by stanParser#returnStmt.
    def exitReturnStmt(self, ctx:stanParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by stanParser#functionDeclsOpt.
    def enterFunctionDeclsOpt(self, ctx:stanParser.FunctionDeclsOptContext):
        pass

    # Exit a parse tree produced by stanParser#functionDeclsOpt.
    def exitFunctionDeclsOpt(self, ctx:stanParser.FunctionDeclsOptContext):
        pass


    # Enter a parse tree produced by stanParser#functionBlock.
    def enterFunctionBlock(self, ctx:stanParser.FunctionBlockContext):
        pass

    # Exit a parse tree produced by stanParser#functionBlock.
    def exitFunctionBlock(self, ctx:stanParser.FunctionBlockContext):
        pass


    # Enter a parse tree produced by stanParser#dataBlock.
    def enterDataBlock(self, ctx:stanParser.DataBlockContext):
        pass

    # Exit a parse tree produced by stanParser#dataBlock.
    def exitDataBlock(self, ctx:stanParser.DataBlockContext):
        pass


    # Enter a parse tree produced by stanParser#transformedDataBlock.
    def enterTransformedDataBlock(self, ctx:stanParser.TransformedDataBlockContext):
        pass

    # Exit a parse tree produced by stanParser#transformedDataBlock.
    def exitTransformedDataBlock(self, ctx:stanParser.TransformedDataBlockContext):
        pass


    # Enter a parse tree produced by stanParser#parametersBlock.
    def enterParametersBlock(self, ctx:stanParser.ParametersBlockContext):
        pass

    # Exit a parse tree produced by stanParser#parametersBlock.
    def exitParametersBlock(self, ctx:stanParser.ParametersBlockContext):
        pass


    # Enter a parse tree produced by stanParser#transformedParametersBlock.
    def enterTransformedParametersBlock(self, ctx:stanParser.TransformedParametersBlockContext):
        pass

    # Exit a parse tree produced by stanParser#transformedParametersBlock.
    def exitTransformedParametersBlock(self, ctx:stanParser.TransformedParametersBlockContext):
        pass


    # Enter a parse tree produced by stanParser#modelBlock.
    def enterModelBlock(self, ctx:stanParser.ModelBlockContext):
        pass

    # Exit a parse tree produced by stanParser#modelBlock.
    def exitModelBlock(self, ctx:stanParser.ModelBlockContext):
        pass


    # Enter a parse tree produced by stanParser#generatedQuantitiesBlock.
    def enterGeneratedQuantitiesBlock(self, ctx:stanParser.GeneratedQuantitiesBlockContext):
        pass

    # Exit a parse tree produced by stanParser#generatedQuantitiesBlock.
    def exitGeneratedQuantitiesBlock(self, ctx:stanParser.GeneratedQuantitiesBlockContext):
        pass


    # Enter a parse tree produced by stanParser#program.
    def enterProgram(self, ctx:stanParser.ProgramContext):
        pass

    # Exit a parse tree produced by stanParser#program.
    def exitProgram(self, ctx:stanParser.ProgramContext):
        pass


