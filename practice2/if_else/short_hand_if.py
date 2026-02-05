#1
a = 8
b = 7
if a > b: print("a is greater than b")

#2
a = 2
b = 3
print("A") if a > b else print("B")

#3
a = 11
b = 22
bigger = a if a > b else b
print("Bigger is", bigger)

#4
a = 44
b = 44
print("A") if a > b else print("=") if a == b else print("B")

#5
x = 17
y = 21
max_value = x if x > y else y
print("Maximum value:", max_value)

#6
username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)
