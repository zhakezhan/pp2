#1
a = 444
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

#2
number = int(input())
if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")

#3
temperature = 22

if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")

#4
username = "Emil"

if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")

#5
age = 16

if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")