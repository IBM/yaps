import graphviz
from . import labeled_strings as labeled_strings

indent_size = 2


class IR(object):
    last_parsed_lineno = 0
    last_parse_col_offset = 0

    def set_map(self, ast):
        if hasattr(ast, 'lineno'):
            self.lineno = ast.lineno
            IR.last_parsed_lineno = ast.lineno
        else:
            self.lineno = IR.last_parsed_lineno
        if hasattr(ast, 'col_offset'):
            self.col_offset = ast.col_offset
            IR.last_parsed_col_offset = ast.col_offset
        else:
            self.col_offset = IR.last_parsed_col_offset

        return self

    def to_stan(self, acc, indent=0):
        acc += self.mkString("NOT YET IMPLEMENTED: " + str(self), indent)

    def mkString(self, str, indent=0):
        return labeled_strings.LabeledString(self, (" "*(indent*indent_size)+str))

    def start_block(self, acc, name, indent=0):
        acc += self.mkString(name + " {", indent)
        acc.newline()

    def end_block(self, acc, indent=0):
        acc += self.mkString("}", indent)
        acc.newline()


class Program(IR):
    # Returns an object that can be converted to a strings
    # or can be indexed as result[line][col] to get the IR object
    # responsible for creating that string
    def to_mapped_string(self):
        ret = labeled_strings.LabeledRope()
        self.to_stan(ret, 0)
        return ret.result()

    def __init__(self, blocks):
        self.blocks = blocks
        self.dot = graphviz.Digraph()
        self.dot.attr('graph', rankdir='LR')

    def viz(self):
        def block_helper(name):
            if (name in self.blocks):
                if name == "parameters" or name == "data" or name == "model":
                    self.blocks[name].viz(self.dot)

        names = [
            "data",
            "transformed_data",
            "parameters",
            "transformed_parameters",
            "model",
            "generated_quantities"]

        for n in names:
            block_helper(n)
        return self.dot

    def to_stan(self, acc, indent=0):
        def block_helper(name):
            if(name in self.blocks):
                self.blocks[name].to_stan(acc, indent)

        names = [
            "data",
            "transformed_data",
            "parameters",
            "transformed_parameters",
            "model",
            "generated_quantities"]

        for n in names:
            block_helper(n)

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

    def viz(self, dot):
        for v in self.vdecls:
            dot.attr('node', shape='circle',
                     style='filled', fillcolor='lightgray')
            dot.node(v.id)

    def to_stan(self, acc, indent=0):
        if self.vdecls:
            self.start_block(acc, "data", indent)
            for b in self.vdecls:
                b.to_stan(acc, indent+1)
                acc.newline()
            self.end_block(acc, indent)


class TransformedDataBlock(ProgramBlock):
    def __init__(self, stmts=[]):
        self.stmts = stmts

    def to_stan(self, acc, indent=0):
        if self.stmts:
            self.start_block(acc, "transformed data", indent)
            for b in self.stmts:
                b.to_stan(acc, indent+1)
                acc.newline()
            self.end_block(acc, indent)


class ParametersBlock(ProgramBlock):
    def __init__(self, vdecls=[]):
        self.vdecls = vdecls

    def viz(self, dot):
        for v in self.vdecls:
            dot.attr('node', shape='circle', style='filled', fillcolor='white')
            dot.node(v.id)

    def to_stan(self, acc, indent=0):
        if self.vdecls:
            self.start_block(acc, "parameters", indent)
            for b in self.vdecls:
                b.to_stan(acc, indent+1)
                acc.newline()
            self.end_block(acc, indent)


class TransformedParametersBlock(ProgramBlock):
    def __init__(self, stmts=[]):
        self.stmts = stmts

    def to_stan(self, acc, indent=0):
        if self.stmts:
            self.start_block(acc, "transformed parameters", indent)
            for b in self.stmts:
                b.to_stan(acc, indent+1)
                acc.newline()
            self.end_block(acc, indent)


class ModelBlock(ProgramBlock):
    def __init__(self, stmts=[]):
        self.stmts = stmts

    def viz(self, dot):
        for stmt in self.stmts:
            stmt.viz(dot)

    def to_stan(self, acc, indent=0):
        if self.stmts:
            self.start_block(acc, "model", indent)
            for b in self.stmts:
                b.to_stan(acc, indent+1)
                acc.newline()
            self.end_block(acc, indent)


class GeneratedQuantities(ProgramBlock):
    def __init__(self, stmts=[]):
        self.stmts = stmts

    def to_stan(self, acc, indent=0):
        if self.stmts:
            self.start_block(acc, "generated quantities", indent)
            for b in self.stmts:
                b.to_stan(acc, indent+1)
                acc.newline()
            self.end_block(acc, indent)

# stmts (Section 5)


class Statement(IR):
    pass


class AssignStmt(Statement):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def to_stan(self, acc, indent=0):
        self.lhs.to_stan(acc, indent)
        assert not self.op, "TODO: handle this"
        acc += self.mkString(" = ")
        self.rhs.to_stan(acc)
        acc += self.mkString(";")


class SamplingStmt(Statement):
    def __init__(self, lhs, dist, trunc=None):
        self.lhs = lhs
        self.dist = dist
        self.trunc = trunc

    def viz(self, dot):
        lv = self.lhs.get_vars()
        dist = self.dist.get_vars()
        for a in lv:
            for b in dist:
                dot.edge(b, a)

    def to_stan(self, acc, indent=0):
        self.lhs.to_stan(acc, indent)
        acc += self.mkString(" ~ ")
        self.dist.to_stan(acc)
        if self.trunc is not None:
            acc += self.mkString(" T")
            acc += self.mkString("[")
            self.trunc.to_stan(acc)
            acc += self.mkString("]")
        acc += self.mkString(";")


class ForStmt(Statement):
    def __init__(self, var, iter, body):
        self.var = var
        self.iter = iter
        self.body = body

    def viz(self, dot):
        for stmt in self.body:
            stmt.viz(dot)

    def iter_to_stan(self, acc):
        acc += self.mkString(" in ")
        if(isinstance(self.iter, Call) and self.iter.id == "range"):
            args = self.iter.args
            if len(args) == 1:
                acc += self.iter.mkString("1:")
                args[0].to_stan(acc)
            elif len(args) == 2:
                args[0].to_stan(acc)
                acc += self.iter.mkString(":")
                args[1].to_stan(acc)
            elif len(args) == 3:
                raise ValueError(
                    "For loop specified using the three argument version of range.  Step values are not currently supported.")
            else:
                raise ValueError(
                    "For loop specified using an invalid invocation of range. range does not accept " + len(args) + " arguments")
        else:
            raise ValueError(
                "For loop specified using an unknown form of iteration.")

    def to_stan(self, acc, indent=0):
        acc += self.mkString("for (", indent)
        self.var.to_stan(acc)
        self.iter_to_stan(acc)
        acc += self.mkString(")")

        if(len(self.body) == 1):
            acc.newline()
            self.body[0].to_stan(acc, indent+1)
        else:
            acc += self.mkString(" {")
            acc.newline()
            for b in self.body:
                b.to_stan(acc, indent+1)
                acc.newline()
            acc += self.mkString("}", indent)


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

    def to_stan(self, acc, indent=0):
        acc += self.mkString(self.id, indent)
        acc += self.mkString("(")
        first = True
        for a in self.args:
            if first:
                first = False
            else:
                acc += self.mkString(",")
            a.to_stan(acc)
        acc += self.mkString(")")


class BreakStmt(Statement):
    pass


class ContinueStmt(Statement):
    pass


# expessions (Section 4)
class Expression(IR):

    def to_stan_prec(self, sub, acc, indent):
        needsParens = sub.precedence > self.precedence
        if needsParens:
            acc += sub.mkString("(", indent)
            sub.to_stan(acc)
            acc += sub.mkString(")")
        else:
            sub.to_stan(acc, indent)

    @property
    def precedence(self):
        return 0


class Atom(Expression):
    def get_vars(self):
        return []


class Constant(Atom):
    def __init__(self, value):
        self.value = value

    def get_vars(self):
        return []

    def to_stan(self, acc, indent=0):
        acc += self.mkString(str(self.value), indent)


class Variable(Atom):
    def __init__(self, id):
        self.id = id

    def get_vars(self):
        return [self.id]

    def to_stan(self, acc, indent=0):
        acc += self.mkString(self.id, indent)


class VectorExpr(Atom):
    pass


class ArrayExpr(Atom):
    pass


class Subscript(Atom):
    def __init__(self, val, slice):
        self.val = val
        self.slice = slice

    def get_vars(self):
        return self.val.get_vars()

    def to_stan(self, acc, indent=0):
        self.to_stan_prec(self.val, acc, indent)
        acc += self.mkString("[")
        self.slice.to_stan(acc)
        acc += self.mkString("]")


class Slice(Expression):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def to_stan(self, acc, indent=0):
        # Do we sometime need parens?
        # is this an operator precedence issue?
        if self.lower:
            self.to_stan_prec(self.lower, acc, indent)
        acc += self.mkString(":")
        if self.upper:
            self.to_stan_prec(self.upper, acc, indent)

    @property
    def precedence(self):
        # not sure
        return 0


class Tuple(Expression):
    def __init__(self, elts):
        self.elts = elts

    def get_vars(self):
        vars = []
        for e in self.elts:
            vars += e.get_vars()
        return vars

    def to_stan(self, acc, indent=0):
        # Do we sometime need parens?
        # is this an operator precedence issue?
        first = True
        for e in self.elts:
            if first:
                first = False
                e.to_stan(acc, indent)

            else:
                acc += self.mkString(", ")
                e.to_stan(acc)


class Binop(Expression):
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def get_vars(self):
        lv = self.lhs.get_vars()
        rv = self.rhs.get_vars()
        return lv + rv

    def to_stan(self, acc, indent=0):
        self.to_stan_prec(self.lhs, acc, indent)
        self.op.to_stan(acc, indent)
        self.to_stan_prec(self.rhs, acc, indent)

    @property
    def precedence(self):
        return self.op.binary_precedence


class Unop(Expression):
    def __init__(self, op, expr):
        self.op = op
        self.rhs = expr

    def get_vars(self):
        return self.rhs.get_vars()

    def to_stan(self, acc, indent=0):
        self.op.to_stan(acc, indent)
        self.to_stan_prec(self.rhs, acc, indent)

    @property
    def precedence(self):
        return self.op.unary_precedence


class Call(Expression):
    def __init__(self, id, args):
        self.id = id
        self.args = args

    def viz(self, dot):
        pass

    def get_vars(self):
        vars = []
        for a in self.args:
            vars += a.get_vars()
        return vars

    def to_stan(self, acc, indent=0):
        acc += self.mkString(self.id, indent)
        acc += self.mkString("(")
        first = True
        for a in self.args:
            if first:
                first = False
            else:
                acc += self.mkString(",")
            a.to_stan(acc)
        acc += self.mkString(")")

# Declarations


class VariableDecl(IR):
    def __init__(self, id, ty, val=None):
        self.id = id
        self.ty = ty
        self.val = val

    def to_stan(self, acc, indent=0):
        if isinstance(self.ty, Type):
            self.ty.decl_to_stan(acc, self.mkString(self.id), indent)
        else:
            self.ty.to_stan(acc, indent)
            acc += self.mkString(" ")
            acc += self.mkString(self.id)

        if self.val is not None:
            acc += self.mkString(" = ")
            self.val.to_stan(acc)
        acc += self.mkString(";")


class Type(IR):
    # All types can print typed variable Declarations
    # ArrayTypes will override this with a custom approach
    def decl_to_stan(self, acc, id, indent=0):
        self.to_stan(acc, indent)
        acc += self.mkString(" ")
        acc += id


class ConstrainedType(Type):
    def __init__(self, cstrts):
        self.cstrts = cstrts

    def constraint_to_stan(self, acc, cstr, indent=0):
        lower, upper = cstr
        acc += self.mkString(str(lower) + "=", indent)
        upper.to_stan(acc)

    def constraints_to_stan(self, acc, indent=0):
        if self.cstrts:
            acc += self.mkString("<", indent)
            first = True
            for cstr in self.cstrts:
                if first:
                    first = False
                else:
                    acc += self.mkString(",")
                self.constraint_to_stan(acc, cstr)

            acc += self.mkString(">")


class AtomicType(ConstrainedType):
    def __init__(self, kind, cstrts=None):
        ConstrainedType.__init__(self, cstrts)
        self.kind = kind

    def to_stan(self, acc, indent=0):
        acc += self.mkString(self.kind, indent)
        self.constraints_to_stan(acc)


class DimType(ConstrainedType):
    def __init__(self, kind, dims, cstrts=None):
        ConstrainedType.__init__(self, cstrts)
        self.kind = kind
        self.dims = dims

    def to_stan(self, acc, indent=0):
        acc += self.mkString(self.kind, indent)
        self.constraints_to_stan(acc)

        if self.dims is not None:
            acc += self.mkString("[")
            self.dims.to_stan(acc)
            acc += self.mkString("]")


class ArrayType(Type):
    def __init__(self, base, dims):
        self.base = base
        self.dims = dims

    # emit a stan typed variable declaration
    def decl_to_stan(self, acc, id, indent=0):
        self.base.to_stan(acc, indent)
        acc += self.mkString(" ")
        acc += id
        if self.dims is not None:
            acc += self.mkString("[")
            self.dims.to_stan(acc)
            acc += self.mkString("]")

# Operator


class Operator(IR):
    pass


class EQ(Operator):
    def __init__(self):
        self.binary_precedence = 7

    def to_stan(self, acc, indent=0):
        acc += self.mkString("==", indent)


class NEQ(Operator):
    def __init__(self):
        self.binary_precedence = 7

    def to_stan(self, acc, indent=0):
        acc += self.mkString("!=", indent)


class SUB(Operator):
    def __init__(self):
        self.binary_precedence = 5
        self.unary_precedence = 1

    def to_stan(self, acc, indent=0):
        acc += self.mkString("-", indent)


class ADD(Operator):
    def __init__(self):
        self.binary_precedence = 5
        self.unary_precedence = 1

    def to_stan(self, acc, indent=0):
        acc += self.mkString("+", indent)


class MULT(Operator):
    def __init__(self):
        self.binary_precedence = 4

    def to_stan(self, acc, indent=0):
        acc += self.mkString("*", indent)


class DIV(Operator):
    def __init__(self):
        self.binary_precedence = 4

    def to_stan(self, acc, indent=0):
        acc += self.mkString("/", indent)


class MOD(Operator):
    def __init__(self):
        self.binary_precedence = 4

    def to_stan(self, acc, indent=0):
        acc += self.mkString("/", indent)
