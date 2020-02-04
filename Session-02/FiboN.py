
def FiboN(n):
    if n < 0:
        print("Incorrect input")
        # First Fibonacci number is 0
    elif n == 1:
        return 0
    # Second Fibonacci number is 1
    elif n == 2:
        return 1
    else:
        return FiboN(n - 1) + FiboN(n - 2)

print(FiboN(11))