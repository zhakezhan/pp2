#1
class Vehicle:
    def move(self):
        print("Vehicle moves")

class Engine:
    def start(self):
        print("Engine starts")

class Car(Vehicle, Engine):
    pass

c = Car()
c.move()   # Vehicle moves
c.start()  # Engine starts

#2
class Employee:
    def work(self):
        print("Working")

class Student:
    def study(self):
        print("Studying")

class Intern(Employee, Student):
    pass

i = Intern()
i.work()   # Working
i.study()  # Studying

#3
class Parent1:
    def greet(self):
        print("Hello from Parent1")

class Parent2:
    def greet(self):
        print("Hello from Parent2")

class Child(Parent1, Parent2):
    def greet(self):
        print("Hello from Child")

c = Child()
c.greet()  # Hello from Child

#4
class Flyer:
    def fly(self):
        print("Flying")

class Swimmer:
    def swim(self):
        print("Swimming")

class Duck(Flyer, Swimmer):
    pass

d = Duck()
d.fly()   # Flying
d.swim()  # Swimming

