import cv2
from src.reader import read_img, print_grid
import operator
import itertools
from collections import Counter

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
        
        symbol = thing[1]
        a = thing[0]
        b = thing[2]
        c = thing[4]
        return operations[symbol](a,b) == c
    
    def get_terms(self):
        return [term for term in self.terms if not isinstance(term, int) and term[0] == 'n']

def find_equations(row):
    eq = []
    curr_eq = []
    for term in row:
        if term != '':
            term = str(term)
            if term.isdigit():
                curr_eq.append(int(term))
            else:
                curr_eq.append(term)
        else:
            curr_eq = []
        if len(curr_eq) == 5:
            eq.append(Equation(curr_eq))
    return eq

def grid_to_equations(grid):
    equations = []
    for row in grid:
        equations.extend(find_equations(row))

    for col in grid.T:
        equations.extend(find_equations(col))
    
    return equations

def solve(available_nums, grid):
    equations = grid_to_equations(grid)

    candidates = {f"n{idx+1}": list(set(available_nums.copy())) for idx, _ in enumerate(available_nums)}
    while True:
        # Filtering: for each equation, constrain the candidates to what could work.
        for curr_term,_ in candidates.items():
            for equation in equations:
                terms = equation.get_terms()
                if not curr_term in terms:
                    continue
                possibilities = [candidates[term] for term in terms]

                all_combinations = []
                for instance in itertools.product(*possibilities):
                    combo_dict = dict(zip(terms, instance))
                    all_combinations.append(combo_dict)

                valid_combinations = [comb for comb in all_combinations if equation.check(comb)]
                candidates[curr_term] = list(set([comb[curr_term] for comb in valid_combinations]))
        
        # If all of a number are used up, don't allow other candidates to use it.
        available_qtys = Counter(available_nums)
        nums_used = {}
        for cand in candidates.values():
            if len(cand) == 1:
                num_used = cand[0]
                nums_used[num_used] = nums_used.get(num_used, 0) + 1
        
        pass
        for k in nums_used.keys():
            if nums_used[k] == available_qtys[k]:
                for cand in candidates.values():
                    if len(cand) != 1:
                        if k in cand:
                            cand.remove(k)

        if all(len(cand) <= 1 for cand in candidates.values()):
            break

    ans = {}
    for k in candidates.keys():
        ans[k] = candidates[k][0]
    return ans