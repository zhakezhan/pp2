#1
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue  # skip the rest for even numbers
    print(i)

#2
i = 0
while i < 10:
    i += 1
    if i % 2 != 0:
        continue  # skip the rest for even numbers
    print(i)

#3
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

#4
i = 0
while i < 15:
    i += 1
    if i % 3 == 0:
        continue
    print(i)

#5
num = 1
while num != 0:
    num = int(input())
    if num < 0:
        print("Negative number skipped!")
        continue
    print(num)

