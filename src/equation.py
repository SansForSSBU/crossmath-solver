import operator

class Equation():
    def __init__(self, terms):
        self.terms = terms
    
    def __str__(self):
        return "".join([str(term) for term in self.terms])

    def __repr__(self):
        return self.__str__()
    
    def check(self, substitutions):
        operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv
        }
        thing = []
        for term in self.terms:
            if term in substitutions.keys():
                thing.append(substitutions[term])
            else:
                thing.append(term)
        
        accumulator = thing[0]
        idx = 1
        while idx < len(thing):
            if idx % 2 == 1:
                operation = thing[idx]
            else:
                operand = thing[idx]
                if operation == "=":
                    return accumulator == operand
                else:
                    accumulator = operations[operation](accumulator, operand)
            idx += 1
    
    def get_terms(self):
        return [term for term in self.terms if not isinstance(term, int) and term[0] == 'n']