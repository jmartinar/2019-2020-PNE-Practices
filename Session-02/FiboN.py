
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

print("The 5th fibonacci number is:", fibon(5))
print("The 10th fibonacci number is:", fibon(10))
print("The 15th fibonacci number is:", fibon(15))
