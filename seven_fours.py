'''
step 0: got the idea from https://puzzling.stackexchange.com/questions/93248/make-expressions-equal-to-100-using-exactly-seven-4s
step 1: 4 possible operators. Will iterate through all possible combinations
of these operators by iterating a base-4 number that is associated with the 
operators.
step 2: Will iterate through all possible parenthetic groupings of the expression.
    - will use prefix notation so the expressions can be represented as binary trees
note: 720 possible groupings for each combination * 4^6 possible operator combinations
= 2949120 possible expressions
'''

operators = ("+","-","*","/")
solutions = []

# doesn't work with digits greater than Z (35), or bases > 36
def number_base_converter(source_number,start_base=10,end_base=3):
    extended_digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    extended_digits = list(extended_digits)
    if start_base != 10:
        base_10_number = 0
        source_number_list = list(str(source_number))
        source_number_list.reverse()
        exponent=0
        for digit in source_number_list:
            if digit in extended_digits:
                digit = 10 + extended_digits.index(digit)
            else:
                digit = int(digit)
            base_10_number += digit*start_base**exponent
            exponent += 1
        source_number = base_10_number
        start_base = 10
    else:
        source_number = int(source_number)
    largest_digit_exponent = 0
    result_number = ""
    import math
    exponent = int(math.log(source_number)/math.log(end_base))
    while exponent >= 0:
        subtracting_number = end_base**exponent
        subtracting_number_multpilicator = int(source_number / subtracting_number)
        if subtracting_number_multpilicator > 9:
            digit_index = subtracting_number_multpilicator - 10
            snm_for_string = extended_digits[digit_index]
        else: snm_for_string = subtracting_number_multpilicator
        result_number+=str(snm_for_string)
        source_number = source_number - subtracting_number_multpilicator * subtracting_number
        exponent-=1
    return result_number

import numpy as np
class BT:
    def __init__(self):
        self.tree = np.zeros((2**7-1),np.int32)
        self.tree[0]=1
    def number_of_leaves(self):
        return int(sum(self.tree==1))

import copy
tree = BT()
def find_trees(tree):
    if tree.number_of_leaves() == 7:
        yield tree.tree
    else:
        leaf_indices = np.argwhere(tree.tree==1).flatten()
        for i in leaf_indices:
            left_child_index = (i+1)*2-1
            right_child_index = (i+1)*2
            #
            tree.tree[i]=2
            tree.tree[left_child_index]=1
            tree.tree[right_child_index]=1
            #
            yield from find_trees(copy.deepcopy(tree))
            #
            tree.tree[left_child_index]=0
            tree.tree[right_child_index]=0
            tree.tree[i]=1

trees_found = []
for i,tree in enumerate(find_trees(tree)):
    tree_list = list(tree)
    if tree_list not in trees_found:
        trees_found.append(tree_list)
        print_tree(tree,i)




