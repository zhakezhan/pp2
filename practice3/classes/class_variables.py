#1
class Dog:
    species = "Canine"  # class variable
    def __init__(self, name):
        self.name = name  # instance variable

d1 = Dog("Buddy")
d2 = Dog("Max")

print(d1.name, d1.species)  # Buddy Canine
print(d2.name, d2.species)  # Max Canine

#2
class Dog:
    species = "Canine"
    
d1 = Dog()
d2 = Dog()

Dog.species = "Wolf"  # changes for all instances

print(d1.species)  # Wolf
print(d2.species)  # Wolf

#3
class Dog:
    species = "Canine"
    def __init__(self, name):
        self.name = name

d1 = Dog("Buddy")
d2 = Dog("Max")

d1.name = "Charlie"  # only changes d1

print(d1.name)  # Charlie
print(d2.name)  # Max

#4
class Dog:
    species = "Canine"

d1 = Dog()
d1.species = "Wolf"  # instance variable overrides class variable

print(d1.species)  # Wolf
print(Dog.species)  # Canine

#5 Modifying Object Properties
class Car:
    def __init__(self, color):
        self.color = color

c = Car("red")
c.color = "blue"
print(c.color)  # blue

#6
class Car:
    pass

c = Car()
c.model = "bmw"
print(c.model)  # bmw

#7 modify property
class Student:
    def __init__(self, gpa):
        self.gpa = gpa

s = Student(3.5)
s.gpa = 4.0
print(s.gpa)  # 4.0

#8
class Dog:
    species = "Canine"

del Dog.species
# print(Dog.species)  # Error! deleted




