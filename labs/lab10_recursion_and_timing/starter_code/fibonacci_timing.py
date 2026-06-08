import time


def fib_recursive(n):
    if n <= 1:
        return n
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n):
    if n <= 1:
        return n
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


def time_function(function, n):
    start_time = time.time()
    function(n)
    end_time = time.time()
    return end_time - start_time


def main():
    values = [5, 10, 20, 25, 30, 35, 40]

    print("Fibonacci Timing")
    print("----------------")
    print("n    recursive_time    iterative_time        speed factor")

    for n in values:
        recursive_time = time_function(fib_recursive, n)
        iterative_time = time_function(fib_iterative, n)
        if iterative_time !=0:
            speed = recursive_time / iterative_time
        print(f"{n:<5} {recursive_time:.8f} seconds    {iterative_time:.8f} seconds     {speed:.1f}")


main()
