#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

#2
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
  
#3
i = 1
while i <= 10:
    if i == 5:
        break
    print(i)
    i += 1

#4
numbers = [3, 7, 2, -1, 4, -5]
for num in numbers:
    if num < 0:
        print(f"Found a negative number: {num}")
        break

#5
while True:
    answer = input("Type 'yes' to continue: ")
    if answer.lower() == "yes":
        print("Thanks!")
        break
    else:
        print("Try again...")
