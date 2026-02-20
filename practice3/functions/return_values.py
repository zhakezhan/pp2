#1
def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)

#2
def my_function():
  return (10, 20)

x, y = my_function()
print("x:", x)
print("y:", y)

#3
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)

#4
def is_even(number):
    return number % 2 == 0

result = is_even(10)
print(result)  # True

result = is_even(7)
print(result)  # False

#5
def greet(name):
    return "Hello, " + name + "!"

message = greet("Alice")
print(message)

