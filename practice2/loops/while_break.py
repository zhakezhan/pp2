#1
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

#2
numbers = [2, 4, 6, 8, 10]

for n in numbers:
    if n == 6:
        print("Found 6!")
        break
    print(n)

#3
count = 0

while count < 10:
    print(count)
    if count == 3:
        print("Stop")
        break
    count += 1

#4
while True:
    password = input()
    if password == "abc123":
        print("Access granted!")
        break
    print("Wrong password, try again.")

#5
i = 1
while True:
    print(i)
    if i == 5:
        break
    i += 1

