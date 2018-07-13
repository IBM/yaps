class IR(object):
    pass


class Program(IR):
    def __init__(self, blocks):
        self.blocks = blocks


# Program Blocks (Section 6)
class ProgramBlock(IR):
    def __init__(self, body=[]):
        self.body = []


class FunctionsBlock(ProgramBlock):
    def __init__(self, fdecls=[]):
        self.fdecls = fdecls


class DataBlock(ProgramBlock):
    def __init__(self, vdecls=[]):
        self.vdecls = vdecls


class TransformedDataBlock(ProgramBlock):
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts


class ParametersBlock(ProgramBlock):
    def __init__(self, vdecls=[]):
        self.vdecls = vdecls


class TransformedParametersBlock(ProgramBlock):
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts


class ModelBlock(ProgramBlock):
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts


class GeneratedQuantities(ProgramBlock):
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts


# Functions (Section 7)
# TODO

# stmts (Section 5)

class Statement(IR):
    pass


class AssignStmt(Statement):
    # TODO add +=, /=, *=, ...
    def __init__(self, lval, exp):
        self.lval = lval
        self.exp = exp


class SamplingStmt(Statement):
    # TODO add `x += f(g | x)`
    def __init__(self, lval, density, args, truncation=None):
        self.lval = lval
        self.density = density
        self.args = args
        self.truncation = truncation


class ForStmt(Statement):
    def __init__(self, id, bounds, stmt):
        self.id = id
        self.bounds = bounds
        self.stmt = stmt


class ConditionalStmt(Statement):
    def __init__(self, cond, exp, alt):
        self.cond = cond
        self.exp = exp
        self.alt = alt


class WhileStmt(Statement):
    def __init__(self, cond, stmt):
        self.cond = cond
        self.stmt = stmt


class Block(Statement):
    pass


class CallStmt(Statement):
    pass


class BreakStmt(Statement):
    pass


class ContinueStmt(Statement):
    pass


# expessions (Section 4)
class expession(IR):
    pass


class Literal(expession):
    pass


class Variable(expession):
    pass


class Vector(expession):
    pass


class Matrix(expession):
    pass


class Array(expession):
    pass


class Conditionalexp(expession):
    pass


class Indexing(expession):
    pass


class Callexp(expession):
    pass


class BinOp(expession):
    pass


# Operators
class Operator(IR):
    pass


class Plus(Operator):
    pass


class Minus(Operator):
    pass


class Pow(Operator):
    pass


class Mult(Operator):
    pass


class Div(Operator):
    pass


class And(Operator):
    pass


class Or(Operator):
    pass


class LE(Operator):
    pass


class GE(Operator):
    pass


class LT(Operator):
    pass


class GT(Operator):
    pass


class EQ(Operator):
    pass
