#Session 2 -- Exercise 3

def fibon(n):
    if n < 0:
        print("Incorrect input")
        # First Fibonacci number is 0
    elif n == 1:
        return 0
    # Second Fibonacci number is 1
    elif n == 2:
        return 1
    else:
        return fibon(n - 1) + fibon(n - 2)


def fibosum(n):
    fibosum  = 0
    for i in range(1, n+1):
        fibosum = fibon(i) + fibosum

    return fibosum

print("The sum of the first 5 fibo terms is:", fibosum(5))
print("The sum of the first 10 fibo terms is:", fibosum(10))