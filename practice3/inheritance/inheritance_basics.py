#Parent class is the class being inherited from, also called base class.
#Child class is the class that inherits from another class, also called derived class.

#1 Create a Parent Class
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()

#2 Create a Child Class
class Student(Person):
  pass 
#Use the pass keyword when you do not want to add any other properties or methods to the class.

#3
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

class Student(Person):
  pass

x = Student("Mike", "Olsen")
x.printname()

#4
class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()  # Some sound

#5
class Vehicle:
    def move(self):
        print("Vehicle moves")

class Car(Vehicle):
    def honk(self):
        print("Beep beep")

c = Car()
c.move()  # Vehicle moves
c.honk()  # Beep beep


