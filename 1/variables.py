#1
x = 5
y = "Nargiz"
print(x)
print(y)

#2
x = 4       # x is of type int
x = "Sally" # x is now of type str
print(x)

#3
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

#4
x = 5
y = "John"
print(type(x))
print(type(y))

#5
a = 4
A = "Sally"
#A will not overwrite a

#6
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)

