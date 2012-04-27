import re
from pyparsing import Literal, Word, alphanums, Optional, nums


class VariableNotFoundException(Exception):
    """raised when a variable was used before asignment"""


class BashArray(list):
    """Simulates bash arrays"""

    def __call__(self, *index):
        if (index == "*") or (index == "@"):
            return self
        elif not index:
            return self[0]
        else:
            return self[index]


class VariableTracker:
    """used to track variables in a shell """

    def __init__(self):
        self.variables = dict()

        def substitute_variables(s, l, t):
            # TODO: get rid of the exception hack
            try:
                if t[1] in self.variables:
                    return self.variables[t[1]]
                else:
                    raise VariableNotFoundException("{} was not declared!".format(t[1]))
            except IndexError:
                if t[0] in self.variables:
                    return self.variables[t[0]]
            raise VariableNotFoundException("{} was not declared!".format(t[0]))

        _simple_var = Literal("$") + Word(alphanums + "_-").setResultsName("varname")
        _brace_substitute_part = Optional("/" + (Word(alphanums + "_-").setResultsName("orig"))
                                 + Optional("/" + Word(alphanums + "_-!?/\\").setResultsName("new")))
        _array_access = "[" + Word(nums + "@*").setResultsName("position") + "]"
        # TODO: parse array correctly
        _brace_var = Literal("${") + Word(alphanums + "_-").setResultsName("text") + _brace_substitute_part + Optional(_array_access) + "}"
        _brace_var.setParseAction(lambda x: x if not x.new else re.sub(x.orig, x.new, x.text))
        self.base_var = _simple_var | _brace_var
        self.var = (Literal('"').suppress() + self.base_var + Literal('"').suppress()) | self.base_var
        self.var.addParseAction(substitute_variables)

    def track_variable(self, varname, value):
        """track a variable, overriding previous existing values"""
        self.variables[varname] = value

    def substitute_variable(self, expression):
        """replace all variables with their respective values, raises an error if one does not exist"""
        return self.var.transformString(expression)
        # what needs to be substituted:
        # $foo, "$foo"
        # ${foo}, "${foo}"
        # ${foo[1]}, ${foo[@]}, ${foo[*]}
