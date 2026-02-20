#1
class MyClass:
  x = 5

p1 = MyClass()
print(p1.x)


#2 Delete the p1 object:
del p1

#3
class Person:
    name = "Anna"

print(Person.name)

#4
class Dog:
    def bark(self):
        print("Woof")

d = Dog()
d.bark()

#5
class Person:
  pass

p1 = Person()
p1.name = "Tobias"
p1.age = 25

print(p1.name)
print(p1.age)
