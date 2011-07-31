
class Switch(dict):
    def __init__(self, cases=None, **kwargs):
        if not cases: 
            cases = {}
        cases = dict(cases)

        dict.__init__(self, cases)
        self.update(**kwargs)

    def match(self, case = None):
        return [key for key in self if case in key]

    def case(self, case, *args):
        results = []
        for expr in self.match(case):
            if hasattr(expr, "__call__"):
                expr_result = expr(*args)
 
        
