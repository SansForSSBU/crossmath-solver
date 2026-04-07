import cv2
from src.reader import read_img
import operator
import itertools
from collections import Counter

def solve(available_nums, board):
    equations = board.get_equations()

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