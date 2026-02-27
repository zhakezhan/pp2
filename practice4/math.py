import math


#Degree to radian
degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)
print("Output radian:", round(radian, 6))


#Area of trapezoid
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area_trapezoid = ((base1 + base2) / 2) * height
print("Expected Output:", area_trapezoid)


#Area of regular polygon
n = int(input("Input number of sides: "))
side = float(input("Input the length of a side: "))

area_polygon = (n * side ** 2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(area_polygon, 2))


#Area of parallelogram
base = float(input("Length of base: "))
height_para = float(input("Height of parallelogram: "))

area_parallelogram = base * height_para
print("Expected Output:", area_parallelogram)