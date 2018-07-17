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

# stmts (Section 5)
class Statement(IR):
    pass

class AssignStmt(Statement):
    def __init__(self, lval, op, exp):
        self.lval = lval
        self.op = op
        self.exp = exp

class SamplingStmt(Statement):
    def __init__(self, lval, op, exp):
        self.lval = lval
        self.op = op
        self.exp = exp

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
    def __init__(self, vdecls=[], stmts=[]):
        self.vdecls = vdecls
        self.stmts = stmts

class CallStmt(Statement):
    def __init__(self, id, args):
        self.id = id
        self.args = args


class BreakStmt(Statement):
    pass


class ContinueStmt(Statement):
    pass


# expessions (Section 4)
class Expession(IR):
    def __init__(self, value):
        self.value = value


# Declarations

class VariableDecl(IR):
    def __init__(self, id, ty, cstr=[], dims=None, exp=None):
        self.id = id
        self.ty = ty
        self.cstr = cstr
        self.dims = dims
        self.exp = exp
