from sly import Lexer, Parser
from collections.abc import Iterable


class PONLexer(Lexer):
    tokens = {"FLOAT", "INTEGER", "STRING", "ID"}

    literals = {'{', '}', '[', ']', ',', ':', '(', ')'}
    ignore_comment = r'\#.*'
    ignore = " \t\n"

    @_(r"['\"](.*?)['\"]")
    def STRING(self, t):
        t.value = t.value.strip("\"'")
        return t

    @_(r"\d+\.\d*")
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r"0b[0-1]+", r"0o[0-7]+", r"0x[0-9a-fA-F]+", r"\d+")
    def INTEGER(self, t):
        if t.value.startswith('0x'):
            t.value = int(t.value[2:], 16)
        elif t.value.startswith("0o"):
            t.value = int(t.value[2:], 8)
        elif t.value.startswith("0b"):
            t.value = int(t.value[2:], 2)
        else:
            t.value = int(t.value)
        return t

    @_(r"[a-zA-Z_][a-zA-Z0-9_]*")
    def ID(self, t):
        match t.value:
            case "True":
                t.value = True
            case "False":
                t.value = False
            case "None":
                t.value = None
        return t


class PONParser(Parser):
    tokens = PONLexer.tokens
    start = "pon"

    @_('object', 'list', 'tuple', 'set')
    def pon(self, p):
        return p[0]

    @_("ID '(' elements ')'")
    def value(self, p):
        match p.ID:
            case "frozenset":
                if len(p.elements) > 1:
                    raise IndexError(f"Too many arguments for a function {p.ID}")
                if not isinstance(p.elements[0], Iterable):
                    raise TypeError(f"Wrong argument type in function {p.ID}. The correct argument type is {Iterable}")
                return frozenset(p.elements[0])

    @_('STRING', 'INTEGER', 'FLOAT')
    def type(self, p):
        return p[0]

    @_('ID')
    def type(self, p):
        if type(p.ID) is not str:
            return p[0]
        raise ValueError(f"Unknown ID '{p.ID}'")

    @_('"{" members "}"')
    def object(self, p):
        return dict(p.members)

    @_('pair')
    def members(self, p):
        return [p.pair]

    @_('pair "," members')
    def members(self, p):
        return [p.pair] + p.members

    @_('type ":" value')
    def pair(self, p):
        return p.type, p.value

    @_('"[" elements "]"')
    def list(self, p):
        return p.elements

    @_('"(" elements ")"')
    def tuple(self, p):
        return tuple(p.elements)

    @_('"{" elements "}"')
    def set(self, p):
        return set(p.elements)

    @_('value')
    def elements(self, p):
        return [p.value]

    @_('value "," elements')
    def elements(self, p):
        return [p.value] + p.elements

    @_('type', 'object', 'list', 'tuple', 'set')
    def value(self, p):
        return p[0]

    def error(self, p):
        raise ValueError(f"Parsing error at token {str(p)}")


lexer = PONLexer()
parser = PONParser()


def load(fp):
    if pon := fp.read():
        return parser.parse(lexer.tokenize(pon))
    else:
        raise ValueError("Empty PON file")


def loads(obj: object):
    return parser.parse(lexer.tokenize(obj))
