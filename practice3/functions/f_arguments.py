#1
def my_function(fname):
  print(fname + " Refsnes")

my_function("Nara")
my_function("Merey")
my_function("Azhar")

#2
#A parameter is the variable listed inside the parentheses in the function definition.
#An argument is the actual value that is sent to the function when it is called.

def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Nara") # "Nara" is an argument

#3
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Nara", "Merey")

#4
def my_function(name = "friend"):
  print("Hello", name)

my_function("Nara")
my_function("Azhar")
my_function() #If the function is called without an argument, it uses the default value
my_function("Merey")

#5
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(animal = "cat", name = "Hero")
#This way, with keyword arguments, the order of the arguments does not matter.

#6
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function("cat", "Hero") #Positional arguments must be in the correct order

#7
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)

#8 Sending a dictionary as an argument:
def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Nara", "age": 18}
my_function(my_person)

#9 Specify positional-only arguments
def my_function(name, /):
  print("Hello", name)

my_function("Nargiz")

#10 Specify keyword-only arguments
def my_function(*, name):
  print("Hello", name)

my_function(name = "Nargiz")

#11
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)