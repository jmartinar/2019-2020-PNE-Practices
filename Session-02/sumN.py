# -- 1 + 2 + 3 + ....... + 20
# -- 1 + .............. + 100


def sumn(n):
    res = 0
    for i in range(1, n+1):
        res = res + i
    return res

print("Sum of 1-20 is:", sumn(20))
print("Sum of 1-100 is:", sumn(100))
