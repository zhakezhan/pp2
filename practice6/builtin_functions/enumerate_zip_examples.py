names = ["A","B","C"]
scores = [10,20,30]

for i, n in enumerate(names):
    print(i, n)

for n, s in zip(names, scores):
    print(n, s)

print(sorted([3,1,2]))

x = "10"
print(int(x), float(x), str(5))