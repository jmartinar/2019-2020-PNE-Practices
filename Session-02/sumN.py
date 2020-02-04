# -- 1 + 2 + 3 + ....... + 20
# -- 1 + .............. + 100

res20 = 0

for x in range(1, 21):
    res20 = res20 + x

print("Sum of 1-20 is:", res20)

res100 = 0

for x in range(1, 101):
    res100 = res100 + x

print("Sum of 1-100 is:", res100)
