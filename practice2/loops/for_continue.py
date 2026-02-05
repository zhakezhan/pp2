#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

#2
for i in range(1, 6):
    if i % 2 == 0:
        continue
    print(i)

#3
numbers = [3, 0, 5]
for n in numbers:
    if n == 0:
        continue
    print(n)

#4
nums = [2, -1, 4]
for n in nums:
    if n < 0:
        continue
    print(n)
    
#5
for letter in "hello":
    if letter == "l":
        continue
    print(letter)

