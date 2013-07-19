import unittest
from execgate import gated_exec, gated_eval, GateSecurityError

class GatedExecTests(unittest.TestCase):
    def test_normal_exec(self):
        locals_dict = {}
        gated_exec('foo = 1 + 1', None, locals_dict)
        self.assertEqual(locals_dict['foo'], 2)

    def test_exec_import_attack(self):
        self.assertRaises(NameError, gated_exec, "__import__('os')")

    def test_exec_underscore_search_attack(self):
        self.assertRaises(GateSecurityError, gated_exec,
"""# courtesy of http://www.reddit.com/r/Python/comments/hftnp/ask_rpython_recovering_cleared_globals/c1v3l4i
lookup = lambda n: [x for x in (1).__class__.__base__.__subclasses__() if x.__name__ == n][0]
try:
    lookup('Codec')().decode('')
except lookup('BaseException') as e:
    del lookup
    __builtins__ = e.__traceback__.tb_next.tb_frame.f_globals['__builtins__']
""")

    def test_normal_eval(self):
        self.assertEqual(gated_eval('1 + 1'), 2)

    def test_eval_import_attack(self):
        self.assertRaises(NameError, gated_eval, "__import__('os')")

    def test_eval_underscore_search_attack(self):
        self.assertRaises(GateSecurityError, gated_eval,
"""# courtesy of http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
[
    c for c in ().__class__.__base__.__subclasses__()
        if c.__name__ == 'catch_warnings'
][0]()._module.__builtins__""")

if __name__ == 'main':
    unittest.main()
