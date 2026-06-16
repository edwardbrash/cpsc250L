import time

import matplotlib.pyplot as plt

def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

def fib_iterative(n):
    # TODO: write this function
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b

    return b

def time_function(function, n):
    # TODO: write this function - google the python time module to figure out how it works
    # TODO: start a timer, call the appropriate function, then stop the timer
    # TODO: return the elapsed time
    start = time.perf_counter()
    function(n)
    end = time.perf_counter()

    return end - start

def main():
    values = [5, 10, 20, 25, 30, 35, 40]

    print("Fibonacci Timing")
    print("----------------")
    print("n    recursive_time    iterative_time")
    rectime = []
    inttime = []
    for n in values:
        recursive_time = time_function(fib_recursive, n)
        iterative_time = time_function(fib_iterative, n)
        rectime.append(recursive_time)
        inttime.append(iterative_time)
        if iterative_time != 0:
            speed = recursive_time/iterative_time
        else:
            speed = float("inf")
        print(f"{n:<5} {recursive_time:.8f} seconds    {iterative_time:.8f} seconds     {speed:.1f}")
    plt.plot(values,rectime, label = "Recursive Time")
    plt.plot(values,inttime, label = "Iterative Time")
    plt.xlabel("n")
    plt.ylabel("Time")
    plt.title("Recursive Time and Iterative Time")
    plt.legend()
    plt.yscale("log")
    plt.show()



    # TODO: create a plot which shows both recursive time and iterative time as a function of n
    # TODO: label the x-axis, y-axis, and provide a title
    # TODO: display a legend that will indicate which dataset is which
    # TODO: make the y-axis logarithmic

main()
