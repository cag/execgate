import ast

class GateSecurityError(Exception): pass

class GatedNodeVisitor(ast.NodeVisitor):
    def visit_Attribute(self, node):
        if('__' in node.attr):
            raise GateSecurityError("Attempting to access private attribute")

def gated_compile(source, filename='<unknown>', mode='exec'):
    code_node = ast.parse(source, filename, mode)
    GatedNodeVisitor().visit(code_node)
    return compile(code_node, filename, mode)

def gated_exec_eval(source, globals={}, locals={}, mode='exec'):
    if globals is None:
        globals = { '__builtins__': {} }
    if globals.get('__builtins__', None) is None:
        globals['__builtins__'] = {}
    if mode is 'exec':
        return exec(gated_compile(source, '<string>', mode), globals, locals)
    elif mode is 'eval':
        return eval(gated_compile(source, '<string>', mode), globals, locals)
    else:
        raise GatedEvalException('invalid mode {}'.format(mode))

def gated_exec(source, globals={}, locals={}):
    gated_exec_eval(source, globals, locals)

def gated_eval(source, globals={}, locals={}):
    return gated_exec_eval(source, globals, locals, 'eval')
