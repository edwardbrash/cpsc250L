def linear_search(values, target):
    comparisons = 0
    for index, value in enumerate(values):
        #print(index, value)
        comparisons += 1
        if value == target:
            return index, comparisons

    return -1, comparisons


def binary_search(values, target):
    comparisons = 0
    index_find = 0
    middle_value = 0
    # implement a binary search tree algorithm
    while len(values) > 1:
        comparisons += 1
        # choose midpoint
        middle_value = values[len(values) // 2]
        #print(middle_value)
        if target > middle_value:
            index_find = index_find + len(values) // 2
            values = values[len(values) // 2:]
            #print("Values: ", values)
            #print("greater ", index_find)
        elif target < middle_value:
            values = values[:len(values) // 2]
            #print("Values: ", values)
            #print("less ", index_find)
        elif target == middle_value:
            index_find = index_find + len(values) // 2
            #print("Values: ", values)
            #print("equal ", index_find)
            return index_find, comparisons
    if middle_value == target:
        return index_find, comparisons
    else:
        return -1, comparisons

def f(x):
    return x * x - 2

def bisection_root(function, left, right, tolerance):
    epsilon = tolerance # tolerance for finding the root
    fa = function(left)
    fb = function(right)
    #print(left, right, fa, fb)
    if abs(fa-fb) < epsilon:
        #print("Type 1: Found root at x = ", left) # ending condition!!!!!!!!
        root = left
    else:
        c = (left+right)/2.0
        fc = function(c)
        if fc == 0.0:
            #print("Type 2: Found root at x = ", c) # second ending condition!!!!
            root = c
        else:
            if fa*fc < 0.0:
                root = bisection_root(function, left, c, tolerance) # recursive call ... first half
            else:
                root = bisection_root(function, c, right, tolerance) # recursive call ... second half

    return root


def main():
    import random
    values = random.sample(range(0, 1000), 500)
    values.sort()

    # Find the 250th value in the list
    search_value = values[249]

    print("Search Tests")
    print("------------")
    print("Linear search for ", search_value," --> (index,comps) = ", linear_search(values, search_value))
    print("Binary search for ", search_value," --> (index,comps) = ", binary_search(values, search_value))

    print()
    print("Root Finding")
    print("------------")
    root = bisection_root(f, 1, 2, 0.0001)
    print("Approximate root of x^2 - 2:", root)


main()
