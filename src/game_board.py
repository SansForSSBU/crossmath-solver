from src.equation import Equation

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
            if len(curr_eq) >= 5:
                eq.append(Equation(curr_eq))
            curr_eq = []
        
    if len(curr_eq) >= 5:
        eq.append(Equation(curr_eq))
    return eq

class GameBoard():
    def __init__(self, np_grid):
        self.np_grid = np_grid

    

    def print(self, max_len=4):
        for row in self.np_grid:
            print(" ".join(f"{str(item):^{max_len}}" for item in row))

    def get_equations(self):
        equations = []
        for row in self.np_grid:
            equations.extend(find_equations(row))

        for col in self.np_grid.T:
            equations.extend(find_equations(col))
        
        return equations
    
    def substitute_answers(self, answers):
        for k, v in answers.items():
            mask = (self.np_grid == k)
            self.np_grid[mask] = v