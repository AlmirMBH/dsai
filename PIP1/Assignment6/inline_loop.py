lst1 = [x * x for x in range(1, 10)]
print(lst1)  # 1, 4, 9, 16, 25, 36, 49

lst2 = [x * x for x in range(1, 10) if x % 2 == 0]
print(lst2)  # 4, 16, 36, 64