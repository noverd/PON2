#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sly import Lexer, Parser
from sly.lex import Token
from sly.yacc import YaccProduction
from collections.abc import Iterable
from typing import Optional

type PONDict = dict | list | tuple | set

type PONTypes = str | int | float

__all__ = ["NamespaceDict", "loader"]

class NamespaceDict(dict):
    def __init__(self, objects: Iterable[object]) -> None:
        super().__init__({obj.__name__ if hasattr(obj, "__name__") else str(obj): obj for obj in objects})

STANDART_NAMESPACE: NamespaceDict = NamespaceDict({False, True, None, str, int, bool, float, dict, list, tuple, set, frozenset})

class PONLexer(Lexer):
    tokens: set[str] = {"FLOAT", "INT", "STR", "ID"}

    literals: set[str] = {'{', '}', '[', ']', ',', ':', '(', ')', '='}
    ignore_comment: str = r'\#.*'
    ignore: str = " \t\n"
    namespace: NamespaceDict

    def __init__(self, namespace: NamespaceDict) -> None: 
        self.namespace = namespace

    @_(r"['\"](.*?)['\"]")
    def STR(self, t: Token) -> Token:
        t.value = t.value.strip("\"'")
        return t

    @_(r"\d+\.\d*")
    def FLOAT(self, t: Token) -> Token:
        t.value = float(t.value)
        return t

    @_(r"0b[0-1]+", r"0o[0-7]+", r"0x[0-9a-fA-F]+", r"\d+")
    def INT(self, t: Token) -> Token:
        if t.value.startswith('0x'):
            t.value: int = int(t.value[2:], 16)
        elif t.value.startswith("0o"):
            t.value: int = int(t.value[2:], 8)
        elif t.value.startswith("0b"):
            t.value: int = int(t.value[2:], 2)
        else:
            t.value: int = int(t.value)
        return t

    @_(r"[a-zA-Z_][a-zA-Z0-9_]*")
    def ID(self, t: Token) -> Token
        try:
            t.value = self.namespace[t.value]
        except KeyError:
            pass
        return t
        


class PONParser(Parser):
    tokens: set[str] = PONLexer.tokens
    start: str = "pon"
    namespace: NamespaceDict

    def __init__(self, namespace: NamespaceDict) -> None: 
        self.namespace = namespace

    @_('dict', 'list', 'tuple', 'set')
    def pon(self, p: YaccProduction) -> PONDict:
        return p[0]

    @_("ID '(' elements ')'")
    def value(self, p: YaccProduction):
        if callable(p.ID):
            return p.ID(*p.elements)
        else:
            raise TypeError("Object {p.ID} is not Callable")

    @_("ID '(' ')'")
    def value(self, p: YaccProduction):
        if callable(p.ID):
            return p.ID()
        else:
            raise TypeError("Object {p.ID} is not Callable")

    @_("ID '(' kwargs ')'")
    def value(self, p: YaccProduction):
        if callable(p.ID):
            return p.ID(**p.kwargs)
        else:
            raise TypeError("Object {p.ID} is not Callable")

    @_("ID '(' elements ',' kwargs ')'")
    def value(self, p: YaccProduction):
        if callable(p.ID):
            return p.ID(*p.elements, **p.kwargs)
        else:
            raise TypeError("Object {p.ID} is not Callable")

    @_('STR', 'INT', 'FLOAT')
    def type(self, p: YaccProduction) -> PONTypes:
        return p[0]

    @_('ID')
    def type(self, p: YaccProduction):
        if type(p.ID) is not str:
            return p[0]
        raise ValueError(f"Unknown ID '{p.ID}'")

    @_('kwarg')
    def kwargs(self, p: YaccProduction) -> dict:
        return p.kwarg

    @_('kwarg ","')
    def kwargs(self, p: YaccProduction) -> dict:
        return p.kwarg

    @_('kwarg "," kwargs')
    def kwargs(self, p: YaccProduction) -> dict:
        return p.kwarg | p.kwargs

    @_('ID "=" value')
    def kwarg(self, p: YaccProduction) -> dict:
        return {p.ID: p.value}

    @_('"{" members "}"')
    def dict(self, p: YaccProduction) -> dict:
        return dict(p.members)

    @_('pair')
    def members(self, p: YaccProduction) -> list:
        return [p.pair]

    @_('pair "," members')
    def members(self, p: YaccProduction) -> list:
        return [p.pair] + p.members

    @_('value ":" value')
    def pair(self, p: YaccProduction) -> tuple:
        return p.value0, p.value1

    @_('"[" elements "]"')
    def list(self, p: YaccProduction) -> list:
        return p.elements

    @_('"(" elements ")"')
    def tuple(self, p: YaccProduction) -> tuple:
        return tuple(p.elements)

    @_('"{" elements "}"')
    def set(self, p: YaccProduction) -> set:
        return set(p.elements)

    @_('value')
    def elements(self, p: YaccProduction) -> list:
        return [p.value]

    @_('value ","')
    def elements(self, p: YaccProduction) -> list:
        return [p.value]

    @_('value "," elements')
    def elements(self, p: YaccProduction) -> list:
        return [p.value] + p.elements

    @_('type', 'dict', 'list', 'tuple', 'set')
    def value(self, p: YaccProduction) -> PONDict | PONTypes:
        return p[0]

    def error(self, p: YaccProduction) -> None:
        raise ValueError(f"Parsing error at token {str(p)}")


class PONLoader:
    lexer: PONLexer
    parser: PONParser

    def __init__(self, namespace: Optional[NamespaceDict] = None):
        if namespace is not None:
            namespace = STANDART_NAMESPACE + namespace
        else:
            namespace = STANDART_NAMESPACE 
        self.lexer = PONLexer(namespace)
        self.parser = PONParser(namespace)

    def parse(self, text: str):
        return self.parser.parse(self.lexer.tokenize(text))

    def load(self, fp) -> PONDict:
        if pon := fp.read():
            return self.parse(pon)
        else:
            raise ValueError("Empty PON file")

    def loads(self, text: str) -> PONDict:
        return self.parse(text)


loader: PONLoader = PONLoader()